import os
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import numpy as np

GENRE_URLs = [
    "https://www.dlsite.com/home/genre/list",
    "https://www.dlsite.com/soft/genre/list",
    "https://www.dlsite.com/maniax/genre/list",
    "https://www.dlsite.com/books/genre/list",
    "https://www.dlsite.com/pro/genre/list"
]

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-javascript")
    
    driver = webdriver.Chrome(options=options)
    return driver

def get_genres():
    driver = create_driver()
    
    genre_list = []
    for url in GENRE_URLs:
        driver.get(url)
        genre_names = driver.find_elements(By.XPATH, '//li[@class="versatility_linklist_item"]')
        genre_urls = driver.find_elements(By.XPATH, '//li[@class="versatility_linklist_item"]/a')
        for genre_name, genre_url in zip(genre_names, genre_urls):
            genre_item = genre_name.get_attribute("textContent")
            genre_item = genre_item.replace('\n', '')
            genre_item = genre_item.replace('  ', '')
            genre_item = genre_item.split('(')[0]
            
            genre_list.append(genre_item)
            print(genre_item)
        
    genre_set = set(genre_list)
    genre_list = list(genre_set)
    
    with open(os.path.join('Genres', 'genre_list.csv'), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(genre_list)
        
def word_to_vec(word, mode):
    pass
        
def get_vector():
    with open(os.path.join('Genres', 'genre_list.csv'), 'r') as f:
        reader = csv.reader(f)
        genre_list = list(reader)[0]
        
    genre_dict = {}
    for i, genre in enumerate(genre_list):
        genre_dict[genre] = word_to_vec(genre, mode='onehot')
        
    np.savez(os.path.join('Genres', 'genre_vecs.npz'), **genre_dict)

if __name__ == "__main__":
    get_genres()
