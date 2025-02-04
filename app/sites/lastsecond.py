from urllib.parse import urlparse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from app.url import detect_hotel_string

lastsecond_crawled_datas = []


def lastsecond_process_url(driver, url):
    if not urlparse(url).path.startswith('/hotels'):
        print('no valid url', url)
        return
    if not detect_hotel_string(urlparse(url).path):
        return
    crawled_data = {'url': url}
    driver.get(url)
    try:
        hotel_name_element = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/h1/span"))
        )
        crawled_data['hotel_name'] = hotel_name_element.text
    except:
        pass
    try:
        room_count_element = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/span"))
        )
        crawled_data['room_count'] = room_count_element.text
    except:
        pass
    try:
        hotel_address_element = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div/div[3]/div[2]"))
        )
        crawled_data['hotel_address'] = hotel_address_element.text
    except:
        pass
    try:
        hotel_stars_element = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]"))
        )
        crawled_data['hotel_stars'] = hotel_stars_element.text
    except:
        pass
    try:
        reviews = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'review-list-item')))
        crawled_data['comments'] = []
        for review in reviews:
            comment = {'profile_name': review.find_element(By.CLASS_NAME, 'upper__profile__name').text,
                       'score_no': review.find_element(By.CLASS_NAME, 'score-no__md').text,
                       'review_body': review.find_element(By.CLASS_NAME,
                                                          'typography.review-list-item__left__body').text}

            crawled_data['comments'].append(comment)
    except Exception as e:
        print(f"Error extracting comments: {url} {e}")


    print(crawled_data)
    if crawled_data['hotel_name'] != "":
        lastsecond_crawled_datas.append(crawled_data)
