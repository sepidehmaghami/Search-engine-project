from soupsieve import match

from app.sites.hotelyar import hotelyar_process_url, hotelyar_crawled_datas
from app.sites.lastsecond import lastsecond_process_url, lastsecond_crawled_datas
from app.sites.eghamat24 import eghamat24_process_url, eghamat24_crawled_datas
from app.sites.site import Site
import json
import os
# Example usage

def get_processor_and_data(url):
    """Returns the appropriate processing function and data based on the URL."""
    processors = {
        "hotelyar.com": (hotelyar_process_url, hotelyar_crawled_datas,'static'),
        "eghamat24.com": (eghamat24_process_url, eghamat24_crawled_datas,'static'),
        "lastsecond.ir": (lastsecond_process_url, lastsecond_crawled_datas,'dynamic'),
    }
    return processors.get(url, (None, None,None))


if __name__ == "__main__":
    url = os.environ.get('URL',"eghamat24.com")
    print(url)
    
    if not url:
        raise ValueError("URL environment variable is not set.")

    process_url, crawled_data,site_type = get_processor_and_data(url)

    if not process_url :
        raise ValueError(f"Unsupported URL: {url}")

    site = Site(url='https://'+url, crawler=site_type)
    site.crawl(process_url)

    output_file = f'{url}.json'
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(crawled_data, file, ensure_ascii=False)

    print(f"Data successfully saved to {output_file}")