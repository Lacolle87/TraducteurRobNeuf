import psycopg
from database.users_postgres import get_connection_str

USERS_CONFIG = 'users_config'
STATS = 'stats_data'


def get_users_configs():
    with psycopg.connect(get_connection_str()) as conn:
        with conn.cursor() as cur:
            cur.execute(f'select * from {USERS_CONFIG}')
            rows = cur.fetchall()
            cols = [description[0] for description in cur.description]
            return cols, rows


def get_stats():
    with psycopg.connect(get_connection_str()) as conn:
        with conn.cursor() as cur:
            cur.execute(f'select * from {STATS}')
            rows = cur.fetchall()
            cols = [description[0] for description in cur.description]
            return cols, rows


print('users_config')
config_cols, config_rows = get_users_configs()
print(*(column.ljust(12) for column in config_cols))
for row in config_rows:
    print(*(str(value)[:14].ljust(12) for value in row))

print('stats_data')
stats_cols, stats_rows = get_stats()
print(*(column.ljust(12) for column in stats_cols))
for row in stats_rows:
    print(*(str(value)[:14].ljust(12) for value in row))
