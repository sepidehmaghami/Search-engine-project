from bs4 import BeautifulSoup
import re
from .general_utils import convert_persian_digits

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
