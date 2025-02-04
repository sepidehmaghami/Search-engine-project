from app.crawlers.dynamic import DynamicCrawler
from app.crawlers.static import StaticCrawler


class Site:
    def __init__(self, url: str, crawler: str):
        self.process_url_func = None
        self.url = url
        if crawler == 'static':
            self.crawler = StaticCrawler()
        else:
            self.crawler = DynamicCrawler()

    def crawl(self,process_url_func):
        self.crawler.crawl(self.url,process_url_func)

    def seed(self):
        self.crawler.seed(self.url)

