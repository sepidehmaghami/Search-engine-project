from main_crawler import get_processor_and_data
from app.sites.site import Site
import os

if __name__ == "__main__":
    url = os.environ.get('URL','eghamat24.com')

    if not url:
        raise ValueError("URL environment variable is not set.")
    _,_,site_type = get_processor_and_data(url)
    site = Site(url='https://'+url, crawler=site_type)
    print(url)
    site.seed()
