import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

hotelyar_crawled_datas = []


def hotelyar_process_url(url):
    if not urlparse(url).path.startswith('/hotel'):
        print('no valid url', url)
        return
    try:
        response = requests.get(url)
    except:
        return
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        crawled_data = {'url':url}
        try:
            crawled_data['name'] = soup.select_one('.ss-hotel-single-hhwt-name').text
            crawled_data['address'] = soup.select_one('div.color-gray:nth-child(2) > span:nth-child(1)').text.strip()  # address
        except Exception:
            pass
        try:
            crawled_data['whole_room_count'] = soup.select_one(
                'div.ss-hotel-single-h-header-features-item:nth-child(3) > div:nth-child(2) > span:nth-child(2)').text  # room count
        except Exception:
            pass
        try:
            crawled_data['height'] = soup.select_one(
                'div.ss-hotel-single-h-header-features-item:nth-child(4) > div:nth-child(2) > span:nth-child(2)').text  # high
        except Exception:
            pass
        try:
            crawled_data['rooms'] = []
            for item in soup.select('.ss-reserve-table > tbody:nth-child(2) tr'):
                room_discount=0
                room_name = item.select_one(
                    'td:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)').text
                room_price = item.select_one('td:nth-child(7) > span:nth-child(1)').text  # price
                try:
                    room_discount = item.select_one('td:nth-child(4) > div:nth-child(1)').text  # discount
                except:
                    pass
                crawled_data['rooms'].append(
                    {'room_name': room_name,'room_price': room_price.strip(), 'room_discount': room_discount.strip()})
        except Exception as e:
            print('rooms failed',url,e)
            pass
        try:
            crawled_data['comments'] = []
            for item in soup.select('#comments-container>div'):
                username = item.select_one(
                    'div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)').text  # username
                score = item.select_one(
                    'div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)').text  # score
                text = item.select_one('div:nth-child(2) > p:nth-child(1)').text  # text
                crawled_data['comments'].append({'username': username, 'score': score, 'text': text})
        except Exception:
            pass
        hotelyar_crawled_datas.append(crawled_data)
        print(crawled_data)


