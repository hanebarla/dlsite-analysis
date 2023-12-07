import os
import json
import argparse
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

SAVE_HISTORY_JSON = 'history.json'
HOME_URL = 'https://www.dlsite.com/home/'
LOGIN_URL = 'https://login.dlsite.com/login?user=self'
LIBARY_URL = 'https://www.dlsite.com/maniax/mypage/userbuy'
NUM_PER_PAGE = 50


def create_args():
    parser = argparse.ArgumentParser(description='DLSite Downloader')
    parser.add_argument('id', help='DLSite ID')
    parser.add_argument('password', help='DLSite Password')

    args = parser.parse_args()

    return args

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-javascript")
    
    driver = webdriver.Chrome(options=options)
    return driver

def login(driver, id, password):
    driver.get(HOME_URL)
    driver.get(LOGIN_URL)

    id_input = driver.find_element(By.XPATH, '//input[@name="login_id"]')
    id_input.send_keys(id)

    password_input = driver.find_element(By.XPATH, '//input[@name="password"]')
    password_input.send_keys(password)

    login_button = driver.find_elements(By.XPATH, '//button[@type="submit"]')
    login_button[0].submit()

    return driver

def get_title_and_url(driver, works):
    work_names = driver.find_elements(By.TAG_NAME, 'dt')
    for work_name in work_names:
        title = work_name.get_attribute("textContent")
        title = title.replace('\n', '')
        title = title.replace('  ', '')
        a_tag = work_name.find_elements(By.TAG_NAME, 'a')
        if len(a_tag) == 0:
            continue
        else:
            url = a_tag[0].get_attribute('href')
            works[title] = {'url': url}
            
def save_dict_to_json(dict, json_path):
    with open(json_path, 'w') as f:
        json.dump(dict, f, indent=4, ensure_ascii=False)
        
def load_dict_from_json(json_path):
    with open(json_path, 'r') as f:
        dict = json.load(f)
    return dict

def get_genre(work_dict):
    driver = create_driver()
    
    for title in work_dict.keys():
        genres = []
        url = work_dict[title]['url']
        driver.get(url)
        
        main_genre = driver.find_elements(By.CLASS_NAME, 'main_genre')
        if len(main_genre) == 0:
            continue
        
        genres_elements = main_genre[0].find_elements(By.TAG_NAME, 'a')
        for genre_element in genres_elements:
            genre = genre_element.get_attribute('textContent')
            genres.append(genre)
        work_dict[title]['genre'] = genres

        print("Title: {}, Genre: {}".format(title, work_dict[title]['genre']))


def get_history():
    args = create_args()
    
    # create driver
    driver = create_driver()
    
    # login
    driver = login(driver, args.id, args.password)
    
    # get history of purchase
    driver.get(LIBARY_URL)
    
    drop_down = driver.find_element(By.XPATH, '//select[@name="start"]')
    select = Select(drop_down)
    select.select_by_value('all')
    display_btn = driver.find_element(By.ID, '_display')
    display_btn.submit()
    time.sleep(10)
    
    html = driver.page_source
    with open('tmp.html', 'w') as f:
        f.write(html)
    
    work_nums = driver.find_element(By.CLASS_NAME, "page_total")
    num_str = work_nums.find_elements(By.TAG_NAME, "strong")
    num_str_txt = num_str[0].get_attribute("textContent")
    whole_work_num = int(num_str_txt)
    page_num = whole_work_num//NUM_PER_PAGE + 1
    print("Work numbers: {}, Page numbers: {}".format(whole_work_num, page_num))
    
    work_dict = {}
    get_title_and_url(driver, work_dict)
    # print(work_contents)
    
    if page_num > 1:
        for i in range(2, page_num+1):
            page_url = LIBARY_URL + '/=/type/all/start/all/sort/1/order/1/page/' + str(i)
            driver.get(page_url)
            get_title_and_url(driver, work_dict)
    
    save_dict_to_json(work_dict, SAVE_HISTORY_JSON)
    print("get history done")
    
    driver.quit()


if __name__ == '__main__':
    get_history()
    work_dict = load_dict_from_json(SAVE_HISTORY_JSON)
    get_genre(work_dict)
    save_dict_to_json(work_dict, SAVE_HISTORY_JSON)
