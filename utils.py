import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time
import re
import json
from url_manager import URLManager

def convert_persian_digits(text):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    latin_digits = '0123456789'
    translation_table = str.maketrans(''.join(persian_digits), ''.join(latin_digits))
    return text.translate(translation_table)

class RobotsParser:
    def __init__(self, base_url):
        self.base_url = base_url
        self.disallowed_paths = []
        self.crawl_delay = 5 
        self._parse_robots()

    def _parse_robots(self):
        robots_url = urljoin(self.base_url, '/robots.txt')
        try:
            response = requests.get(robots_url, headers=HEADERS, timeout=10)
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

def extract_hotel_data(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    hotel = {
        "url": url,
        "name": extract_name(soup),
        "star_rating": extract_stars(soup),
        "rating": extract_overall_rating(soup),
        "reviews_count": extract_reviews_count(soup),
        "rooms": extract_rooms(soup),
        "comments": extract_comments(soup)
    }
    return hotel

def extract_name(soup):
    name_tag = soup.find('h1')
    if not name_tag:
        name_tag = soup.find('div', class_='property-title')  # مثال
    return name_tag.get_text(strip=True) if name_tag else None

def extract_stars(soup):
    stars_div = soup.find('span', class_='hotel_star')
    if stars_div:
        meta = stars_div.find('meta', itemprop='ratingValue')
        if meta and 'content' in meta.attrs:
            try:
                return int(meta['content'])
            except ValueError:
                pass
    return 0


def extract_overall_rating(soup):
    rating_div = soup.find('div', class_='d-flex align-items-center')
    if rating_div:
        rating = rating_div.find('span', class_='subtitle-2 text-black')
        if rating:
            text = convert_persian_digits(rating.get_text(strip=True))
            try:
                return float(text)
            except:
                return None
    return None

def extract_reviews_count(soup):
    count_tag = soup.find('span', class_='body-2 fw-semibold text-secondary')
    if count_tag:
        text = convert_persian_digits(count_tag.get_text())
        match = re.search(r'\d+', text)
        return int(match.group()) if match else 0
    return 0

def extract_rooms(soup):
    rooms = []
    room_sections = soup.find_all('div', class_='card-body d-flex flex-wrap flex-lg-nowrap align-items-stretch')
    
    for section in room_sections:
        room = {
            "type": extract_room_type(section),
            "capacity": extract_capacity(section),
            "board_type": extract_board_type(section),
            "price": extract_room_price(section),
            "original_price": extract_original_price(section),
            "discount": extract_discount(section),
            "amenities": extract_room_amenities(section)
        }
        rooms.append(room)
    return rooms

def extract_room_type(section):
    type_tag = section.find('span', class_='js-room-type-name')
    return type_tag.get_text(strip=True) if type_tag else None

def extract_capacity(section):
    capacity_tag = section.find('div', class_='d-flex flex-wrap body-2 mb-3 mb-md-2')
    if capacity_tag:
        text = capacity_tag.get_text()
        text = convert_persian_digits(text)
        match = re.search(r'(\d+)\s*نفره', text)
        return int(match.group(1)) if match else None
    return None

def extract_board_type(section):
    board_tag = section.find('span', class_='p-room__board-type')
    return board_tag.get_text(strip=True) if board_tag else None

def extract_room_price(section):
    price_tag = section.find('div', class_='subtitle-3 fw-semibold fw-md-bold')
    if price_tag:
        text = convert_persian_digits(price_tag.get_text())
        return int(''.join(filter(str.isdigit, text)))
    return None

def extract_original_price(section):
    original_tag = section.find('span', class_='text-decoration-line-through')
    if original_tag:
        text = convert_persian_digits(original_tag.get_text())
        return int(''.join(filter(str.isdigit, text)))
    return None

def extract_discount(section):
    discount_tag = section.find('span', class_='badge badge-plain body-1 fw-bold text-success py-0')
    if discount_tag:
        return discount_tag.get_text(strip=True)
    return None

def extract_room_amenities(section):
    amenities = []
    amenities_tags = section.find_all('button', class_='chip chip-border')
    for tag in amenities_tags:
        amenities.append(tag.get_text(strip=True))
    return amenities

def extract_comments(soup):
    comments = []
    comments_section = soup.find('div', id='property-comments', class_='property-comments__comments')
    
    if comments_section:
        for comment in comments_section.find_all('div', class_='card js-comment js-travel-goal-family mb-5'):
            comment_data = {
                "user": extract_comment_user(comment),
                "rating": extract_comment_rating(comment),
                "date": extract_comment_date(comment),
                "text": extract_comment_text(comment),
                "type": extract_comment_type(comment)
            }
            comments.append(comment_data)
    return comments

def extract_comment_user(comment):
    user_tag = comment.find('div', class_='fw-semibold me-2 me-md-4')
    return user_tag.get_text(strip=True) if user_tag else None

def extract_comment_rating(comment):
    rating_tag = comment.find('span', class_='body-1 fw-semibold')
    if rating_tag:
        text = convert_persian_digits(rating_tag.get_text(strip=True))
        try:
            return float(text.split('/')[1].strip())
        except:
            return None
    return None

def extract_comment_date(comment):
    date_tags = comment.find_all('div', class_='text-secondary')
    if len(date_tags) >= 2:
        return date_tags[1].get_text(strip=True)
    return None

def extract_comment_text(comment):
    text_tags = comment.find_all('div', class_='property-comments__comment-text body-1')
    texts = [tag.get_text(strip=True) for tag in text_tags]
    return "\n".join(texts) if texts else None

def extract_comment_type(comment):
    type_tag = comment.find('div', class_='text-secondary')
    return type_tag.get_text(strip=True) if type_tag else None

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
                
            with open('eghamat24.json', 'w', encoding='utf-8') as f:
                json.dump(all_hotels_data, f, indent=2, ensure_ascii=False, default=str)
            
            print("Data successfully saved to hotels.json")

        except Exception as e:
            print(f"Main error: {str(e)}")

if __name__ == "__main__":
    main()
