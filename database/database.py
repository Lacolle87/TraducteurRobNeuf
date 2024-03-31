import psycopg
import logging
from config_data.config import load_config

USERS_CONFIG = 'users_config'
STATS = 'stats_data'

db_connection = None


def get_connection():
    global db_connection
    if db_connection is None:
        try:
            config = load_config()
            logging.info("Creating a new database connection...")
            db_connection = psycopg.connect(dbname=config.db.database,
                                            user=config.db.db_user,
                                            password=config.db.db_password,
                                            host=config.db.db_host)
            logging.info("Database connection created successfully.")
        except psycopg.Error as e:
            logging.error(f"Error creating database connection: {e}.")
    else:
        logging.info("Reusing existing database connection...")
    return db_connection


def create_tables(conn):
    try:
        with conn.cursor() as conn:
            conn.execute(f'''create table if not exists {USERS_CONFIG} (
                                id serial primary key,
                                hashed_user_id text unique,
                                src_lang text,
                                dest_lang text
                              )''')

            conn.execute(f'''create table if not exists {STATS} (
                                id serial primary key,
                                hashed_user_id text,
                                src_lang text,
                                dest_lang text,
                                created_at timestamp,
                                foreign key (hashed_user_id) references {USERS_CONFIG} (hashed_user_id)
                              )''')
        logging.info(f"Database tables: «{USERS_CONFIG}», «{STATS}» created or verified.")
    except Exception as e:
        logging.error(f"Error initializing database: {e}.")


def close_database():
    global db_connection
    if db_connection:
        try:
            db_connection.close()
            logging.info("Database connection closed.")
        except Exception as e:
            logging.error(f"Error closing database connection: {e}.")
    else:
        logging.warning("No open database connection to close or connection is already closed.")
