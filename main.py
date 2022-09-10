import time
import random

from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By

import psycopg2
from config import host, user, password, db_name


string = None

class SearchVacancies:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.pages = None

    def parsing_names(self):
        """Ищет названия вакансий и ссылки на них
        После этого сохраняет в базу данных PostgreSQL"""
        try:
            db.count_strings()
            # db.delete_table()  # deleting a table
            # db.create_table()  # creating a table
            search_name = ['django']  # по каким тегам ищутся вакансии
            db.start_db()
            self.transition_to_links()

            for url in search_name:
                self.driver.get(f'https://kirov.hh.ru/search/vacancy?text={url}')  # вписывает в поле слово вакансии
                time.sleep(random.randrange(5, 10))

                self.amount_pages()  # считает количество страниц

                for page in range(self.pages):  # переходит с одной страницы на другую
                    self.driver.get(
                        f'https://kirov.hh.ru/search/vacancy?text=django&from=suggest_post&salary=&clusters=true&ored_clusters=true&enable_snippets=true&page={page}&hhtmFrom=vacancy_search_list')

                    self.driver.find_elements(By.CLASS_NAME, 'bloko-link')  # ищет класс, в котором содержатся названия вакансий
                    elements = self.driver.find_elements(By.TAG_NAME, 'a')  # ищет элементы с тегом "а"

                    for element in elements:  # перебирает все элементы, которые спарсились
                        if ('Python' in element.text) or ('Django' in element.text):  # если в названии вакансии есть определенные слова
                            name = element.text  # выводит текст названия вакансии
                            url = element.get_attribute('href')  # находит ссылки на вакансии
                            db.insert_date(name, url)  # записывает

            self.driver.close()  # closing the browser
            db.close_db()  # close connection with PostgreSQL

        except Exception as _ex:
            self.driver.close()
            db.close_db()
            print(f"[ERROR] {_ex}")

    def amount_pages(self):
        """Ищет количество страниц на сайте"""

        self.driver.find_element(By.CLASS_NAME, 'pager')  # ищет элемент класса (чтобы посчитать количество страниц)

        # записывает в переменную количество страниц на сайте
        pages = self.driver.find_element(By.CSS_SELECTOR,
                                    '#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > div.main-content > div > div:nth-child(3) > div.sticky-sidebar-and-content--NmOyAQ7IxIOkgRiBRSEg > div.bloko-column.bloko-column_xs-4.bloko-column_s-8.bloko-column_m-9.bloko-column_l-13 > div > div.bloko-gap.bloko-gap_top > div > span:nth-child(6) > span.pager-item-not-in-short-range > a > span')
        self.pages = int(pages.text)  # преобразовывает текст в числовой формат
        print(self.pages)

    def transition_to_page(self):
        """Переходит на каждую страницу на сайте"""

        for i in range(self.pages):  # переходит с одной ссылки (страницы) на другую
            self.driver.get(f'https://kirov.hh.ru/search/vacancy?text=django&from=suggest_post&salary=&clusters=true&ored_clusters=true&enable_snippets=true&page={i}&hhtmFrom=vacancy_search_list')

    def transition_to_links(self):
        """Goes to each vacancy by links from the database
        and parses data from it"""

        # iterates over all links in a table
        for num in range(1, 11):
            print(num)
            self.driver.get(db.following_a_link(num))  # clicks to links for each vacancy in a table
            self.driver.find_element(By.CLASS_NAME, 'g-user-content')
            elements = self.driver.find_elements(By.CSS_SELECTOR, '#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > div.main-content > div > div > div > div > div.bloko-column.bloko-column_container.bloko-column_xs-4.bloko-column_s-8.bloko-column_m-12.bloko-column_l-10 > div:nth-child(3) > div > div > div:nth-child(1) > div')

            for element in elements:
                element = element.text.lower()
                name = db.vacancy_name(num).lower()

                print(name)

                if ('стажер' in [name or element]) or ('trainee' in [name or element]):
                    print('trainee')

                if ('junior' in (name or element)) or ('джуниор' in (name, element)) or ('джун' in (name, element)):
                    print('junior')

                if ('middle' in (name or element)) or ('mid' in (name, element)) or ('мидл' in (name, element)) or ('миддл' in (name, element)):
                    print('middle')

                if ('senior' in [name or element]) or ('сеньор' in [name or element]) or ('синьор' in [name or element]):
                    print('senior')

            time.sleep(random.randrange(3, 7))


class DataBase:

    def __init__(self):
        self.string = None
        self.connection = None
        self.cursor = None
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
            self.cursor = self.connection.cursor()  # defines the cursor
            self.connection.autocommit = True  # enable autosave data

            self.cursor.execute('SELECT version();')  # writing a version PostgreSQL
            print(f'Server version: {self.cursor.fetchone()}')

        except Exception as _ex:
            print('[INFO] Error while working with PostgreSQL', _ex)
            self.connection.close()  # closing the PostgreSQL

    def insert_date(self, name, url):
        """Insert data into table"""

        self.cursor.execute(
            f"""INSERT INTO vacancies (vacancy_name, link_to_vacancy) VALUES
            ('{name}', '{url}');"""
        )
        print('[INFO] Data was successfully inserted')

    def count_strings(self):
        """Counts the number of rows in a table"""

        self.cursor.execute("SELECT count(*) FROM vacancies;")
        strings = self.cursor.fetchone()
        return int(strings[0])  # number of rows in a table

    def following_a_link(self, num):

        self.cursor.execute(f"SELECT link_to_vacancy FROM vacancies WHERE id = '{num}';")
        links = self.cursor.fetchone()
        return links[0]



    def vacancy_name(self, num):
        self.cursor.execute(f"SELECT vacancy_name FROM vacancies WHERE id = '{num}';")
        name = self.cursor.fetchone()
        return name[0]



    def create_table(self):
        """Creating a new table"""

        # create a new table
        self.cursor.execute(
            """CREATE TABLE vacancies(
                id serial PRIMARY KEY,
                vacancy_name varchar(100) NOT NULL,
                link_to_vacancy text NOT NULL,
                trainee text,
                junior text,
                middle text,
                senior text);"""
        )
        print('[INFO] Table created successfully')

    def delete_table(self):
        """Deleting a table"""

        self.cursor.execute("DROP TABLE vacancies;")
        print('[INFO] Table was deleted')

    def close_db(self):
        """Close connection with PostgreSQL"""

        self.cursor.close()
        self.connection.close()
        print('[INFO] PostgreSQL connection closed')


search = SearchVacancies()
db = DataBase()

if __name__ == '__main__':
    search.parsing_names()
else:
    print('ERROR')
