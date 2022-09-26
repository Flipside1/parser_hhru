import re
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# import psycopg2
# import configuration as config
from database import db
string = None


class Parsing:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.pages = None

    def parsing_names(self):
        """Searches for job titles and links to them
        After that, it saves them to the database."""
        try:
            db.count_strings()  # page count on request

            db.delete_table()  # deleting a table
            db.create_table()  # creating a table
            search_name = ['django', 'python', 'developer', 'разработчик', 'программист']  # tags to vacancy

            db.start_db()

            for url in search_name:
                self.driver.get(f'https://kirov.hh.ru/search/vacancy?text={url}')  # enters the vacancy tag in the field
                time.sleep(random.randrange(3, 5))

                self.amount_pages()  # counts the number of pages

                for page in range(self.pages):  # moves from one page to another
                    self.driver.get(
                        f'https://kirov.hh.ru/search/vacancy?text=django&from=suggest_post&salary=&clusters=true&ored_clusters=true&enable_snippets=true&page={page}&hhtmFrom=vacancy_search_list')

                    try:
                        elements = WebDriverWait(self.driver, 2).until(
                            EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
                        )  # searching "a" tag

                        for element in elements:  # iterates over all elements that are parsed
                            if ('Python' in element.text) or ('Django' in element.text):  # filters vacancy titles
                                name = element.text  # displays the text of the vacancy title
                                url = element.get_attribute('href')  # finds a link to this vacancy
                                db.insert_name_and_link(name, url)  # writes to database
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
        """Looks for the number of pages on the site"""

        self.driver.find_element(By.CLASS_NAME, 'pager')  # looks for a class element (to count the number of pages)

        # writes to a variable the number of pages on the site
        pages = self.driver.find_element(By.CSS_SELECTOR,
                                         '#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > div.main-content > div > div:nth-child(3) > div.sticky-sidebar-and-content--NmOyAQ7IxIOkgRiBRSEg > div.bloko-column.bloko-column_xs-4.bloko-column_s-8.bloko-column_m-9.bloko-column_l-13 > div > div.bloko-gap.bloko-gap_top > div > span:nth-child(6) > span.pager-item-not-in-short-range > a > span')
        self.pages = int(pages.text)  # converts str to int
        print(self.pages)

    def transition_to_page(self):
        """Goes to every page on the site"""

        for i in range(self.pages):  # moves from one page of the site to another
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

            try:
                # self.driver.implicitly_wait(3)
                WebDriverWait(self.driver.get(link), 10)  # clicks to links for each vacancy in a table
                # self.driver.get(link)  # clicks to links for each vacancy in a table

            except TimeoutException as _te:
                print(_te)
                print('[ERROR] LINK')

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
                    print('[ERROR] DESCRIPTION')

            def required_experience():
                """getting element from the required experience class"""

                try:
                    experience_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > div.main-content > div > div > div > div > div.bloko-column.bloko-column_container.bloko-column_xs-4.bloko-column_s-8.bloko-column_m-12.bloko-column_l-10 > div:nth-child(1) > div.bloko-column.bloko-column_xs-4.bloko-column_s-8.bloko-column_m-12.bloko-column_l-10 > div > p:nth-child(3) > span'))
                    )

                    nums = re.sub(r'[^0-9–]+', r'', experience_element.text)  # removes all characters except 0-9 and –
                    return nums

                except Exception as _ex:
                    print(_ex)
                    print('[ERROR] REQUIRED EXPERIENCE')

            def key_skills():
                """getting elements from the key skills class"""

                nonlocal skills
                skills = []
                for number in range(1, 31):

                    try:
                        element = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, f'/html/body/div[5]/div/div[3]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div[3]/div[2]/div/div[{number}]/span'))
                        )
                        skill = element.text
                        skills.append(skill)
                    except Exception as _ex:
                        break

                if len(skills) < 1:  # checking if elements are in a list
                    skills = [0]
                print(num, skills)

            def company_name():
                """looking for company name"""

                element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > div.main-content > div > div > div > div > div.bloko-column.bloko-column_container.bloko-column_xs-4.bloko-column_s-8.bloko-column_m-12.bloko-column_l-10 > div:nth-child(2) > div > div.bloko-column.bloko-column_xs-4.bloko-column_s-8.bloko-column_m-12.bloko-column_l-6 > div > div > div > div.vacancy-company-details > span > a > span'))
                )
                name = element.text
                return name

            experience = required_experience()
            description()  # calls variables: trainee, junior, middle, senior
            key_skills()  # list of skills
            c_name = company_name()

            db.insert_other_data(c_name, experience, trainee, junior, middle, senior, skills, num)
            time.sleep(random.randrange(2, 5))


parsing = Parsing()

if __name__ == '__main__':
    parsing.parsing_names()
else:
    print('ERROR')
