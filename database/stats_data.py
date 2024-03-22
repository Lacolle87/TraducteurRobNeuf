import sqlite3
from services.services import hash_user_id

DATABASE_FILE = 'database/users.db'
USERS_CONFIG = 'users_config'
STATS = 'stats_data'


def create_stats():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''create table if not exists {STATS} (
                            id integer primary key,
                            hashed_user_id integer,
                            src_lang text,
                            dest_lang text,
                            created_at timestamp,
                            foreign key (hashed_user_id) references {USERS_CONFIG} (hashed_user_id)
                          )''')
        conn.commit()


def save_stats(users_config):
    create_stats()
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        try:
            conn.execute('begin transaction')
            for user_id, config in users_config.items():
                src_lang = config['src_lang']
                dest_lang = config['dest_lang']
                hashed_user_id = hash_user_id(user_id)
                cursor.execute(f'''
                        insert into {STATS}  (hashed_user_id, src_lang, dest_lang, created_at)
                        values (?, ?, ?, current_timestamp)
                    ''', (hashed_user_id, src_lang, dest_lang))
            conn.commit()
        except sqlite3.Error as e:
            print('Error:', e)
            conn.rollback()
