import time, random
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

urls = ['https://kirov.hh.ru/search/vacancy?text=django', 'https://kirov.hh.ru/search/vacancy?text=python']  # Какие url ищутся
driver = webdriver.Firefox()

def open_hh():
    """Ищет названия вакансий"""

    for url in urls:
        print(url)
        driver.get(url=url)
        time.sleep(random.randrange(5, 10))

        driver.find_elements(By.CLASS_NAME, 'bloko-link')
        elements = driver.find_elements(By.TAG_NAME, 'a')
        for element in elements:
            if ('Python' in element.text) or ('Django' in element.text):
                print(element.text)

    driver.close()

open_hh()