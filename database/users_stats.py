import logging
import psycopg
from database.database import get_connection

USERS_CONFIG = 'users_config'
STATS = 'stats_data'


def create_stats_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute(f'''create table if not exists {STATS} (
                            id serial primary key,
                            hashed_user_id text,
                            src_lang text,
                            dest_lang text,
                            created_at timestamp,
                            foreign key (hashed_user_id) references {USERS_CONFIG} (hashed_user_id)
                          )''')
            conn.commit()
        logging.info("Stats table created successfully.")
    except psycopg.Error as e:
        logging.error(f"Error creating stats table: {e}.")


def save_stats(users_config):
    with get_connection() as conn:
        create_stats_table(conn)
        try:
            with conn.cursor() as cur:
                for hashed_user_id, config in users_config.items():
                    src_lang = config['src_lang']
                    dest_lang = config['dest_lang']
                    cur.execute(f'''
                    insert into {STATS} (hashed_user_id, src_lang, dest_lang, created_at)
                    values (%s, %s, %s, current_timestamp)
                    ''', (hashed_user_id, src_lang, dest_lang))
                conn.commit()
            logging.info("Stats saved successfully.")
        except psycopg.Error as e:
            logging.error(f"Error saving stats: {e}.")
            conn.rollback()
