import psycopg
import logging
from config_data.config import load_config

USERS_CONFIG = 'users_config'
STATS = 'stats_data'


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.config = load_config()
            self.db_connection = None
            self._initialize_connection()
            self._initialized = True

    def _initialize_connection(self):
        if self.db_connection is None:
            try:
                logging.info("Creating a new database connection...")
                self.db_connection = psycopg.connect(
                    dbname=self.config.db.database,
                    user=self.config.db.db_user,
                    password=self.config.db.db_password,
                    host=self.config.db.db_host
                )
                logging.info("Database connection created successfully.")
            except psycopg.Error as e:
                logging.error(f"Error creating database connection: {e}.")

    def get_connection(self):
        if self.db_connection is not None:
            logging.info("Reusing existing database connection...")
            return self.db_connection
        else:
            self._initialize_connection()
            return self.db_connection

    def create_tables(self):
        try:
            with self.get_connection().cursor() as cursor:
                cursor.execute(f'''CREATE TABLE IF NOT EXISTS {USERS_CONFIG} (
                                    id SERIAL PRIMARY KEY,
                                    hashed_user_id TEXT UNIQUE,
                                    src_lang TEXT,
                                    dest_lang TEXT
                                  )''')

                cursor.execute(f'''CREATE TABLE IF NOT EXISTS {STATS} (
                                    id SERIAL PRIMARY KEY,
                                    hashed_user_id TEXT,
                                    src_lang TEXT,
                                    dest_lang TEXT,
                                    created_at TIMESTAMP,
                                    FOREIGN KEY (hashed_user_id) REFERENCES {USERS_CONFIG} (hashed_user_id)
                                  )''')
                self.db_connection.commit()
            logging.info(f"Database tables: «{USERS_CONFIG}», «{STATS}» created or verified.")
        except Exception as e:
            logging.error(f"Error initializing database: {e}.")

    def close_database(self):
        if self.db_connection:
            try:
                self.db_connection.close()
                logging.info("Database connection closed.")
            except Exception as e:
                logging.error(f"Error closing database connection: {e}.")
        else:
            logging.warning("No open database connection to close or connection is already closed.")
