import time
import random

from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By


import psycopg2
from config import host, user, password, db_name


driver = webdriver.Firefox()

class Search_vacancies:

    def __init__(self):
        self.pages = None
        self.counter = 1  # счетчик, нужен для вписывания элемента в определенную строку таблицы
        self.start_bd()

    def parsing_names(self):
        """Ищет названия вакансий и ссылки на них
        После этого сохраняет в таблицу Excel"""

        search_name = ['django']  # по каким тегам ищутся вакансии

        for url in search_name:
            driver.get(f'https://kirov.hh.ru/search/vacancy?text={url}')  # вписывает в поле слово вакансии
            time.sleep(random.randrange(5, 10))

            self.amount_pages()  # считает количество страниц

            for page in range(self.pages):  # переходит с одной страницы на другую
                driver.get(
                    f'https://kirov.hh.ru/search/vacancy?text=django&from=suggest_post&salary=&clusters=true&ored_clusters=true&enable_snippets=true&page={page}&hhtmFrom=vacancy_search_list')

                driver.find_elements(By.CLASS_NAME, 'bloko-link')  # ищет класс, в котором содержатся названия вакансий
                elements = driver.find_elements(By.TAG_NAME, 'a')  # ищет элементы с тегом "а"

                for element in elements:  # перебирает все элементы, которые спарсились
                    if ('Python' in element.text) or ('Django' in element.text):  # если в названии вакансии есть определенные слова
                        self.counter += 1  # счетчик +1 каждый раз
                        name = element.text  # выводит текст названия вакансии
                        url = element.get_attribute('href')  # находит ссылки на вакансии
                        with self.connection.cursor() as cursor:
                            cursor.execute(
                                f"""INSERT INTO vacancies (vacancy_name, link_to_vacancy) VALUES
                                ('{name}', '{url}');"""
                            )

                            print('[INFO] Data was successfully inserted')

        driver.close()  # закрывает браузер

    def amount_pages(self):
        """Ищет количество страниц на сайте"""
        driver.find_element(By.CLASS_NAME, 'pager')  # ищет элемент класса (чтобы посчитать количество страниц)
        # записывает в переменную количество страниц на сайте
        pages = driver.find_element(By.CSS_SELECTOR,
                                    '#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > div.main-content > div > div:nth-child(3) > div.sticky-sidebar-and-content--NmOyAQ7IxIOkgRiBRSEg > div.bloko-column.bloko-column_xs-4.bloko-column_s-8.bloko-column_m-9.bloko-column_l-13 > div > div.bloko-gap.bloko-gap_top > div > span:nth-child(6) > span.pager-item-not-in-short-range > a > span')
        self.pages = int(pages.text)  # преобразовывает текст в числовой формат
        print(self.pages)

    def transition_to_page(self):
        """Переходит на каждую страницу на сайте"""
        for i in range(self.pages):  # переходит с одной ссылки (страницы) на другую
            driver.get(f'https://kirov.hh.ru/search/vacancy?text=django&from=suggest_post&salary=&clusters=true&ored_clusters=true&enable_snippets=true&page={i}&hhtmFrom=vacancy_search_list')

    def start_bd(self):

        try:
            #
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            self.connection.autocommit = True

            with self.connection.cursor() as cursor:
                cursor.execute('SELECT version();')
                print(f'Server version: {cursor.fetchone()}')

        except Exception as _ex:
            print('[INFO] Error while working with PostgreSQL', _ex)
            self.connection.close()


search = Search_vacancies()

if __name__ == '__main__':
    search.parsing_names()
else:
    print('ERROR')


# except Exception as _ex:
#     print('[INFO] Error while working with PostgreSQL', _ex)
#
# finally:
#     if connection:
#         connection.close()
#         print('[INFO] PostgreSQL connection closed')