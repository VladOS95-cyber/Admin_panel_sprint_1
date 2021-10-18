import logging
import os.path
import os
import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from DataMigration import PostgresSaver, SQLiteLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db.sqlite")


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""

    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    logging.info('Loading data')
    data = sqlite_loader.load_movies()
    logging.info('Data from db.sqlite saved sucessfully')

    logging.info('Save data into postgre database')
    postgres_saver.save_all_data(data)
    logging.info('All data saved sucessfully')


if __name__ == '__main__':
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': 'localhost',
        'port': 5432,
        'options': '-c search_path=content'}
    with sqlite3.connect(DB_PATH) as sqlite_conn, psycopg2.connect(
        **dsl, cursor_factory=DictCursor
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
