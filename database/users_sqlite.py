import sqlite3

DATABASE_FILE = 'users_config.db'
TABLE_NAME = 'users_config'


def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f'''create table if not exists {TABLE_NAME} (
                        user_id integer primary key,
                        src_lang text,
                        dest_lang text
                      )''')
    conn.commit()
    conn.close()


def load_users_config():
    create_table()
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f'select * from {TABLE_NAME}')
    rows = cursor.fetchall()
    users_config = {}
    for row in rows:
        user_id, src_lang, dest_lang = row
        users_config[str(user_id)] = {'src_lang': src_lang, 'dest_lang': dest_lang}
    conn.close()
    return users_config


def save_users_config(users_config):
    create_table()
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    for user_id, config in users_config.items():
        src_lang = config['src_lang']
        dest_lang = config['dest_lang']
        cursor.execute(f'''
                    INSERT OR REPLACE INTO {TABLE_NAME} (user_id, src_lang, dest_lang)
                    VALUES (?, ?, ?)
                ''', (user_id, src_lang, dest_lang))
    conn.commit()
    conn.close()


def select_all_data():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {TABLE_NAME}')
    rows = cursor.fetchall()
    conn.close()
    return rows


for row in select_all_data():
    print(*row)
