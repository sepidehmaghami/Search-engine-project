import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time
import re

def convert_persian_digits(text):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    latin_digits = '0123456789'
    translation_table = str.maketrans(''.join(persian_digits), ''.join(latin_digits))
    return text.translate(translation_table)

class RobotsParser:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.disallowed_paths = []
        self.crawl_delay = 5 
        self.headers = headers if headers else {}
        self._parse_robots()

    def _parse_robots(self):
        robots_url = urljoin(self.base_url, '/robots.txt')
        try:
            response = requests.get(robots_url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                self._process_robots_txt(response.text)
        except Exception as e:
            print(f"Error parsing robots.txt: {str(e)}")

    def _process_robots_txt(self, content):
        current_user_agent = None
        for line in content.split('\n'):
            line = line.strip().lower()
            if line.startswith('user-agent:'):
                current_user_agent = line.split(':')[1].strip()
            elif line.startswith('disallow:') and current_user_agent == '*':
                path = line.split(':')[1].strip()
                self.disallowed_paths.append(path)
            elif line.startswith('crawl-delay:') and current_user_agent == '*':
                try:
                    self.crawl_delay = max(self.crawl_delay, int(line.split(':')[1].strip()))
                except:
                    pass

    def is_allowed(self, url):
        parsed = urlparse(url)
        for path in self.disallowed_paths:
            if parsed.path.startswith(path):
                return False
        return True

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7',
}