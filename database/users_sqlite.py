import sqlite3
from cachetools import cached, TTLCache
from services.services import hash_user_id

DATABASE_FILE = 'database/users.db'
USERS_CONFIG = 'users_config'

cache = TTLCache(maxsize=100, ttl=300)


def create_table():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''create table if not exists {USERS_CONFIG} (
                            hashed_user_id text primary key,
                            src_lang text,
                            dest_lang text
                          )''')
        conn.commit()


@cached(cache=cache)
def load_users_config():
    create_table()
    users_config = {}
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(f'select hashed_user_id, src_lang, dest_lang from {USERS_CONFIG}')
        rows = cursor.fetchall()
        for row in rows:
            hashed_user_id, src_lang, dest_lang = row
            users_config[str(hashed_user_id)] = {'src_lang': src_lang, 'dest_lang': dest_lang}
    return users_config


def save_users_config(users_config):
    create_table()
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        try:
            conn.execute('begin transaction')
            for hashed_user_id, config in users_config.items():
                src_lang = config['src_lang']
                dest_lang = config['dest_lang']
                cursor.execute(f'''
                        insert or replace into {USERS_CONFIG}  (hashed_user_id, src_lang, dest_lang)
                        values (?, ?, ?)
                    ''', (hashed_user_id, src_lang, dest_lang))
            conn.commit()
        except sqlite3.Error as e:
            print('Error:', e)
            conn.rollback()
