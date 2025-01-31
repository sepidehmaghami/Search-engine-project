import time
import requests
from urllib.parse import urlparse
import json
import os
from utils import RobotsParser, extract_links, extract_hotel_data
from url_manager import URLManager
from storage import DataStorage
from elasticsearch import Elasticsearch
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configure logging
logging.basicConfig(
    filename='crawler.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class Crawler:
    def __init__(self, redis_host='redis', redis_port=6379, queue_key='url_queue',
                 visited_key='visited_urls', output_dir='data', elastic_host='elasticsearch', elastic_port=9200):
        self.url_manager = URLManager(redis_host, redis_port, queue_key, visited_key)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # ایجاد نمونه DataStorage
        self.data_storage = DataStorage(output_dir=self.output_dir, elastic_host=elastic_host, elastic_port=elastic_port)
        
        self.elasticsearch = self.data_storage.elasticsearch  # اگر نیاز دارید به Elasticsearch دسترسی داشته باشید
        self._setup_elasticsearch()
        self.domain_last_access = {}
        self.robots_parsers = {}

        # Selenium setup
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def _setup_elasticsearch(self):
        if not self.elasticsearch.indices.exists(index="hotels"):
            self.elasticsearch.indices.create(index="hotels")
            logging.info("Elasticsearch index 'hotels' created.")

    def crawl(self):
        while self.url_manager.has_urls():
            url = self.url_manager.get_url()
            if not url:
                break
            domain = urlparse(url).netloc
            if domain not in self.robots_parsers:
                self.robots_parsers[domain] = RobotsParser(f"{urlparse(url).scheme}://{domain}")

            robots = self.robots_parsers[domain]
            if not robots.is_allowed(url):
                logging.info(f"URL disallowed by robots.txt: {url}")
                continue

            # Respect crawl delay
            last_access = self.domain_last_access.get(domain, 0)
            delay = robots.crawl_delay
            elapsed = time.time() - last_access
            if elapsed < delay:
                sleep_time = delay - elapsed
                logging.info(f"Sleeping for {sleep_time} seconds before accessing {domain}")
                time.sleep(sleep_time)

            try:
                logging.info(f"Crawling URL: {url}")
                response = self.fetch_page(url)
                if response:
                    hotel_data = extract_hotel_data(response.text, url)
                    if hotel_data['name']:  # Assuming name is mandatory
                        # استفاده از DataStorage برای ذخیره و ایندکس داده‌ها
                        self.data_storage.process_data(hotel_data)
                        
                        new_links = extract_links(response.text, url)
                        for link in new_links:
                            self.url_manager.add_url(link)
                self.domain_last_access[domain] = time.time()
            except Exception as e:
                logging.error(f"Error processing URL {url}: {e}")

    def fetch_page(self, url):
        try:
            response = requests.get(url, timeout=10)
            if 'text/html' in response.headers.get('Content-Type', ''):
                return response
            else:
                logging.warning(f"Non-HTML content at {url}")
                return None
        except requests.RequestException as e:
            logging.error(f"Request failed for {url}: {e}")
            return None

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    crawler = Crawler()
    try:
        crawler.crawl()
    finally:
        crawler.close()
