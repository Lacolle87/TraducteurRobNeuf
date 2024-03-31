import logging
import psycopg
from database.database import Database

STATS = 'stats_data'


def save_stats(stats_data):
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cur:
            for hashed_user_id, stats in stats_data.items():
                src_lang = stats['src_lang']
                dest_lang = stats['dest_lang']
                cur.execute(f'''
                    INSERT INTO {STATS} (hashed_user_id, src_lang, dest_lang, created_at)
                    VALUES (%s, %s, %s, current_timestamp)
                    ''', (hashed_user_id, src_lang, dest_lang))
            conn.commit()
        logging.info("Stats saved successfully.")
    except psycopg.Error as e:
        logging.error(f"Error saving stats: {e}.")
        conn.rollback()
        logging.exception("Error traceback:")
