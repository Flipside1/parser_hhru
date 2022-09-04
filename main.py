import time, random

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Firefox()

name_list = []
url_list = []
dictionary = {}

def open_hh():
    """Ищет названия вакансий"""
    search_name = ['django', 'python', 'selenium', 'sql', 'backend']  # по каким тегам ищутся вакансии

    for url in search_name:
        driver.get(f'https://kirov.hh.ru/search/vacancy?text={url}')
        time.sleep(random.randrange(5, 10))

        driver.find_elements(By.CLASS_NAME, 'bloko-link')
        elements = driver.find_elements(By.TAG_NAME, 'a')
        for element in elements:

            if ('Python' in element.text) or ('Django' in element.text):
                name = element.text  # выводит текст названия вакансии
                url = element.get_attribute('href')  # находит ссылки на вакансии
                dictionary[name] = url

    print(dictionary)
    driver.close()


open_hh()