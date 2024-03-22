import sqlite3

DATABASE_FILE = 'users_config.db'
USERS_CONFIG = 'users_config'


def select_all_data():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(f'select * from {USERS_CONFIG}')
        rows = cursor.fetchall()
    return rows


[print(*row) for row in select_all_data()]
