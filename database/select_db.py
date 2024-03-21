import sqlite3

DATABASE_FILE = 'users_config.db'
TABLE_NAME = 'users_config'


def select_all_data():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f'select * from {TABLE_NAME}')
    rows = cursor.fetchall()
    conn.close()
    return rows


[print(*row) for row in select_all_data()]
