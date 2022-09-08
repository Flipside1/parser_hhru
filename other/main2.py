import psycopg2
from config import host, user, password, db_name

try:
    pass
except Exception as _ex:
    print("[INFO] Error while with PostgreSQL", _ex)
finally:
    pass