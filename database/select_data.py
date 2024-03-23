import sqlite3

DATABASE_FILE = 'users.db'
USERS_CONFIG = 'users_config'
STATS = 'stats_data'

agg_by_scr = f'select hashed_user_id, src_lang, count(*) as count_all from {STATS} group by 1, 2 order by 3 desc'
agg_by_dest = f'select user_id, dest_lang, count(*) as count_all from {STATS} group by 1, 2 order by 3 desc'


def select_all_data():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(f'select * from {USERS_CONFIG}')
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
    return columns, rows


column_names, rows = select_all_data()

print(*(column.ljust(4) for column in column_names))
for row in rows:
    print(*(str(value).ljust(4) for value in row))
