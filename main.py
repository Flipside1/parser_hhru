import time
import random

from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By

import psycopg2
from config import host, user, password, db_name


driver = webdriver.Firefox()


class SearchVacancies:

    def __init__(self):
        self.pages = None
        self.counter = 1  # счетчик, нужен для вписывания элемента в определенную строку таблицы

    def parsing_names(self):
        """Ищет названия вакансий и ссылки на них
        После этого сохраняет в базу данных PostgreSQL"""

        # db.delete_table()  # deleting a table
        # db.create_table()  # creating a table
        search_name = ['django']  # по каким тегам ищутся вакансии
        db.start_db()

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
                        db.insert_date(name, url)  # записывает

        driver.close()  # closing the browser
        db.close_db()  # close connection with PostgreSQL

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

    def transition_to_links(self):
        pass


class DataBase:

    def __init__(self):
        self.connection = None
        self.start_db()

    def start_db(self):
        """Connecting to PostgreSQL"""

        try:
            # connecting to PostgreSQL
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            self.connection.autocommit = True  # enable autosave data

            # writing a version PostgreSQL
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT version();')
                print(f'Server version: {cursor.fetchone()}')

        except Exception as _ex:
            print('[INFO] Error while working with PostgreSQL', _ex)
            self.connection.close()  # closing the PostgreSQL

    def create_table(self):
        """Creating a new table"""

        # create a new table
        with self.connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE vacancies(
                    id serial PRIMARY KEY,
                    vacancy_name varchar(100) NOT NULL,
                    link_to_vacancy text NOT NULL);"""
            )
            print('[INFO] Table created successfully')
        
    def insert_date(self, name, url):
        """Insert data into table"""

        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO vacancies (vacancy_name, link_to_vacancy) VALUES
                ('{name}', '{url}');"""
            )
            print('[INFO] Data was successfully inserted')

    def delete_table(self):
        """Deleting a table"""

        with self.connection.cursor() as cursor:
            cursor.execute(f"""DROP TABLE vacancies;""")
            print('[INFO] Table was deleted')

    def close_db(self):
        """Close connection with PostgreSQL"""

        self.connection.close()
        print('[INFO] PostgreSQL connection closed')




search = SearchVacancies()
db = DataBase()

if __name__ == '__main__':
    search.parsing_names()
else:
    print('ERROR')
