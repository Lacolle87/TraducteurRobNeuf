import io
import csv
import psycopg
from datetime import datetime
from services.services import hash_file_data
from database.users_postgres import get_connection_str

STATS = 'stats_data'


def get_stats():
    with psycopg.connect(get_connection_str()) as conn:
        with conn.cursor() as cur:
            cur.execute(f'select * from {STATS}')
            rows = cur.fetchall()
            cols = [description[0] for description in cur.description]
            return cols, rows


def stats_to_csv(columns, data):
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(columns)
        writer.writerows(data)
        csv_data = output.getvalue()
        return csv_data
    except (io.UnsupportedOperation, csv.Error):
        return None


def generate_filename(data):
    data_to_hash = [','.join(map(str, row)) for row in data]
    hashed_data = hash_file_data('\n'.join(data_to_hash))[-4:]
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_name = f'stats_data_{current_date}_{hashed_data}.csv'
    return file_name
