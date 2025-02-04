from selenium import webdriver
from selenium.webdriver.firefox.service import Service

from app.crawlers.base import BaseCrawler
from app.redis_queue.queue import Queue
from selenium.webdriver.common.by import By
from urllib.parse import  urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.firefox.options import Options
from app.url import normalize_url, get_robots_txt_disallowed_urls


class DynamicCrawler(BaseCrawler):

    def __init__(self):
        self.disallow_urls = None
        self.queue = Queue('127.0.0.1', 6379)
        self.name = 1
        firefox_options = Options()
        firefox_options.add_argument('--headless')

        service = Service('C:\\Users\\Fatemeh\\geckodriver.exe')
        driver = webdriver.Firefox(service=service, options=firefox_options)



        self.driver = driver

    def crawl(self, main_url,process_url_func):
        self.disallow_urls = get_robots_txt_disallowed_urls(main_url)

        while True:
            u = self.queue.pop_from_queue(self.name)
            if u is None:
                print('all urls done')
                break
            if u in self.disallow_urls:
                continue
            process_url_func(self.driver, u)

            urls = self.derive_urls(u)
            for url in urls:
                if not urlparse(url).path.startswith('/hotels'):
                    continue
                self.queue.push_to_queue(self.name, url)
            time.sleep(0.5)  # be polite

    def seed(self, main_url):

        urls = self.derive_urls(main_url)
        for url in urls:
            self.queue.push_to_queue(self.name, url)

    def derive_urls(self, url):
        base_domain = urlparse(url).netloc

        try:
            self.driver.get(url)
            local_hrefs = []
            wait = WebDriverWait(self.driver, 20)  # Wait up to 10 seconds
            a_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
            hrefs = [link.get_attribute('href') for link in a_elements if link.get_attribute('href')]
            for href in hrefs:
                if href.startswith('#'):
                    continue
                normalized_href = normalize_url(url, href)

                if urlparse(normalized_href).netloc == base_domain:
                    local_hrefs.append(normalized_href)
            return local_hrefs

        except:
            return []
