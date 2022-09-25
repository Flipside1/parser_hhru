import psycopg2
import configuration as config


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
                host=config.host,
                user=config.user,
                password=config.password,
                database=config.db_name
            )
            self.cursor = self.connection.cursor()  # defines the cursor
            self.connection.autocommit = True  # enable autosave data

            self.cursor.execute('SELECT version();')  # writing a version PostgreSQL
            print(f'Server version: {self.cursor.fetchone()}')

        except Exception as _ex:
            print('[INFO] Error while working with PostgreSQL', _ex)
            self.connection.close()  # closing the PostgreSQL

    def insert_name_and_link(self, name, url):
        """Insert data into table
        (names and urls)"""

        try:
            self.cursor.execute(
                f"""INSERT INTO vacancies (vacancy_name, link_to_vacancy) VALUES
                ('{name}', '{url}');"""
            )
        except Exception as _ex:
            print('[ERROR]', _ex)

    def insert_other_data(self, company_name, experience, trainee, junior, middle, senior, skills, num):
        """Insert data into table
        (experience, skills)"""

        self.cursor.execute(
            f"""UPDATE vacancies SET 
            company_name = '{company_name}',
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
        """follows the link to vacancy from the database"""

        self.cursor.execute(f"SELECT link_to_vacancy FROM vacancies WHERE id = '{num}';")
        links = self.cursor.fetchone()
        return links[0]

    def vacancy_name(self, num):
        """takes the name of the job to filter the skills in the
        "SearchVacancies" class in the "description" function"""

        self.cursor.execute(f"SELECT vacancy_name FROM vacancies WHERE id = '{num}';")
        name = self.cursor.fetchone()
        return name[0]

    def duplicate_deleting(self):
        """Removes all duplicate vacancies"""

        self.cursor.execute(
            """DELETE FROM vacancies WHERE id NOT IN 
            (SELECT MIN(id) FROM vacancies GROUP BY link_to_vacancy);"""
        )

    def create_table(self):
        """Creating a new table"""

        # create a new table
        self.cursor.execute(
            """CREATE TABLE vacancies(
                id serial PRIMARY KEY,
                vacancy_name varchar(100) NOT NULL,
                link_to_vacancy text NOT NULL,
                company_name text,
                required_experience text,
                trainee text,
                junior text,
                middle text,
                senior text,
                key_skills text[]);"""
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


db = DataBase()
