from abc import ABC, abstractmethod
class BaseCrawler(ABC):

    @abstractmethod
    def crawl(self,main_url,process_url_func):
        pass

    @abstractmethod
    def seed(self,main_url):
        pass

    @abstractmethod
    def derive_urls(self, url):
        pass