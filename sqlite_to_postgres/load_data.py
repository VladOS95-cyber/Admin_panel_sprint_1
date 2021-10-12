import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
import os.path


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "db.sqlite")    
    dsl = {'dbname': 'movies', 'user': 'postgres', 'password': 'postgres', 'host': 'localhost', 'port': 5432}
    with sqlite3.connect(db_path) as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
