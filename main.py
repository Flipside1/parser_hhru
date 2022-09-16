import re
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
            db.count_strings()  # page count on request

            # db.delete_table()  # deleting a table
            # db.create_table()  # creating a table
            search_name = ['django', 'python', 'developer', 'разработчик', 'программист']  # по каким тегам ищутся вакансии

            db.start_db()

            for url in search_name:
                self.driver.get(f'https://kirov.hh.ru/search/vacancy?text={url}')  # вписывает в поле слово вакансии
                time.sleep(random.randrange(3, 5))

                self.amount_pages()  # считает количество страниц

                for page in range(self.pages):  # переходит с одной страницы на другую
                    self.driver.get(
                        f'https://kirov.hh.ru/search/vacancy?text=django&from=suggest_post&salary=&clusters=true&ored_clusters=true&enable_snippets=true&page={page}&hhtmFrom=vacancy_search_list')

                    try:
                        elements = WebDriverWait(self.driver, 2).until(
                            EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
                        )  # searching "a" tag

                        for element in elements:  # перебирает все элементы, которые спарсились
                            if ('Python' in element.text) or ('Django' in element.text):  # если в названии вакансии есть определенные слова
                                name = element.text  # выводит текст названия вакансии
                                url = element.get_attribute('href')  # находит ссылки на вакансии
                                db.insert_name_and_link(name, url)  # записывает названия и ссылки
                    except Exception as _ex:
                        print(_ex)

                self.transition_to_links()

            db.duplicate_deleting()  # removes duplicate lines
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
        """goes to each vacancy by links from the database
        and parses data from it"""

        trainee = None
        junior = None
        middle = None
        senior = None

        skills = [0, 0, 0]

        # iterates over all links in a table
        for num in range(1, db.count_strings()+1):

            link = db.following_a_link(num)
            self.driver.get(link)  # clicks to links for each vacancy in a table

            def description():
                """getting elements from the description class"""

                try:
                    description_elements = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > div.main-content > div > div > div > div > div.bloko-column.bloko-column_container.bloko-column_xs-4.bloko-column_s-8.bloko-column_m-12.bloko-column_l-10 > div:nth-child(3) > div > div > div:nth-child(1) > div'))
                    )  # elements on description

                    for element in description_elements:

                        nonlocal trainee, junior, middle, senior  # updates the value of variables

                        element = element.text.lower()  # makes all letters in text small
                        name = db.vacancy_name(num).lower()

                        trainee = 0
                        junior = 0
                        middle = 0
                        senior = 0

                        # if the given words are in the text or vacancy name, then updates the value of the variable to 1
                        if ('стажер' in name) or ('trainee' in name) or \
                                ('стажер' in element) or ('trainee' in element):
                            trainee = 1
                        if ('junior' in name) or ('джуниор' in name) or ('джун' in name) or \
                                ('junior' in element) or ('джуниор' in element) or ('джун' in element):
                            junior = 1
                        if ('middle' in name) or ('mid' in name) or ('мидл' in name) or ('миддл' in name) or \
                                ('middle' in element) or ('mid' in element) or ('мидл' in element) or ('миддл' in element):
                            middle = 1
                        if ('senior' in name) or ('сеньор' in name) or ('синьор' in name) or \
                                ('senior' in element) or ('сеньор' in element) or ('синьор' in element):
                            senior = 1
                except Exception as _ex:
                    print(_ex)

            def required_experience():

                try:
                    experience_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > div.main-content > div > div > div > div > div.bloko-column.bloko-column_container.bloko-column_xs-4.bloko-column_s-8.bloko-column_m-12.bloko-column_l-10 > div:nth-child(1) > div.bloko-column.bloko-column_xs-4.bloko-column_s-8.bloko-column_m-12.bloko-column_l-10 > div > p:nth-child(3) > span'))
                    )

                    nums = re.sub(r'[^0-9–]+', r'', experience_element.text)  # removes all characters except 0-9 and –
                    return nums

                except Exception as _ex:
                    print(_ex)

            def key_skills():
                nonlocal skills
                skills = []

                for number in range(1, 31):

                    try:
                        element = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, f'div:nth-child(3) > div > div:nth-child({number}) > span'))
                        )
                        element = element.text
                        skills.append(element)
                    except Exception as _ex:
                        break

                if len(skills) < 2:
                    skills = [0, 0]  # checking if elements are in a list
                print(num, skills)

            experience = required_experience()
            description()  # calls variables: trainee, junior, middle, senior
            key_skills()  # call list

            db.insert_other_data(experience, trainee, junior, middle, senior, skills, num)
            time.sleep(random.randrange(2, 5))


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

    def insert_name_and_link(self, name, url):
        """Insert data into table"""  # имена и ссылки

        try:
            self.cursor.execute(
                f"""INSERT INTO vacancies (vacancy_name, link_to_vacancy) VALUES
                ('{name}', '{url}');"""
            )
        except Exception as _ex:
            print('[ERROR]', _ex)

    def insert_other_data(self, experience, trainee, junior, middle, senior, skills, num):
        self.cursor.execute(
            f"""UPDATE vacancies SET 
            required_experience = '{experience}', 
            trainee = '{trainee}', 
            junior = '{junior}', 
            middle = '{middle}', 
            senior = '{senior}',
            key_skills = ARRAY {skills}
            WHERE id = '{num}';"""
        )      # ARRAY -> massive

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
                required_experience text,
                trainee text,
                junior text,
                middle text,
                senior text,
                key_skills text[]);"""
        )
        print('[INFO] Table created successfully')

    def duplicate_deleting(self):
        """Removes all duplicate vacancies"""

        self.cursor.execute(
            """DELETE FROM vacancies WHERE id NOT IN 
            (SELECT MIN(id) FROM vacancies GROUP BY link_to_vacancy);"""
        )

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
