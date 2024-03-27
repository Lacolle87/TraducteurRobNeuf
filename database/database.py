import psycopg
import logging
from config_data.config import load_config

db_connection = None


def get_connection():
    global db_connection
    if db_connection is None or db_connection.closed != 0:
        try:
            config = load_config()
            db_connection = psycopg.connect(dbname=config.db.database,
                                            user=config.db.db_user,
                                            password=config.db.db_password,
                                            host=config.db.db_host)
            logging.info("Creating a new database connection...")
        except psycopg.Error as e:
            logging.error(f"Error creating database connection: {e}")
    else:
        logging.info("Reusing existing database connection...")

    return db_connection
