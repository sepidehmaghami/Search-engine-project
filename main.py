import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time
import json
from url_manager import URLManager
from utils.general_utils import RobotsParser, HEADERS
from utils.eghamat24_utils import extract_hotel_data


def main():
    # base_url = "https://www.eghamat24.com/IranHotels.html"
    url_manager  = URLManager()  
    base_url = url_manager.get_url() 
    all_hotels_data = []  

    with requests.Session() as session:
        session.headers.update(HEADERS)
        
        try:
            # Get main page
            response = session.get(base_url)
            response.raise_for_status()
            
            # Parse robots.txt
            robots = RobotsParser(base_url)
            
            # Extract hotel links
            soup = BeautifulSoup(response.text, 'html.parser')
            hotel_links = set()
            
            for card in soup.find_all('article', class_='property-card-vertical'):
                link = card.find('a', href=True)
                if link:
                    full_url = urljoin(base_url, link['href'])
                    if robots.is_allowed(full_url):
                        hotel_links.add(full_url)
            
            # Process each hotel
            for url in list(hotel_links)[:3]:  # Limit for testing
                try:
                    time.sleep(robots.crawl_delay)
                    response = session.get(url)
                    response.raise_for_status()
                    
                    hotel_data = extract_hotel_data(response.text, url)
                    # print(json.dumps(hotel_data, indent=2, ensure_ascii=False, default=str))
                    all_hotels_data.append(hotel_data)
                    
                except Exception as e:
                    print(f"Error processing {url}: {str(e)}")

            json_folder = './json'
            os.makedirs(json_folder, exist_ok=True)
            json_path = os.path.join(json_folder, 'eghamat24.json')                
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(all_hotels_data, f, indent=2, ensure_ascii=False, default=str)
            
            print("Data successfully saved to hotels.json")

        except Exception as e:
            print(f"Main error: {str(e)}")

if __name__ == "__main__":
    main()
