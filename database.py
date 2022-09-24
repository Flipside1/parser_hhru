import psycopg2
from configuration import host, user, password, db_name


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

    # insert data into a table
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO vacancies (vacancy_name, link_to_vacancy) VALUES
            ('{arg1}', '{arg2}');"""
        )

        print('[INFO] Data was successfully inserted')


except Exception as _ex:
    print('[INFO] Error while working with PostgreSQL', _ex)

finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')
