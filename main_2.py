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

    # create a new table
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE users(
                id serial PRIMARY KEY,
                first_name varchar[100] NOT NULL,
                nick_name varchar[100] NOT NULL);"""
        )

        print('[INFO] Table created successfully')



except Exception as _ex:
    print('[INFO] Error while working with PostgreSQL', _ex)

finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')
