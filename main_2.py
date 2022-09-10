import psycopg2
from config import host, user, password, db_name


try:
    # connecting with postgres
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    # create cursor
    with connection.cursor() as cursor:
        cursor.execute('SELECT version();')
        print(f'Server version: {cursor.fetchone()}')

    # # create a new table
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """CREATE TABLE vacancies(
    #             id serial PRIMARY KEY,
    #             vacancy_name varchar(50) NOT NULL,
    #             link_to_vacancy text NOT NULL);"""
    #     )
    #
    #     print('[INFO] Table created successfully')

    # insert data into a table
    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT INTO vacancies (vacancy_name, link_to_vacancy) VALUES
            ('Maxim', 'FLIPSIDE'), ('Oleg', 'Troll');"""
        )

        print('[INFO] Data was successfully inserted')


except Exception as _ex:
    print('[INFO] Error while working with PostgreSQL', _ex)

finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')
