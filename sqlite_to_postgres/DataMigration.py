from Dataclasses import Film_work, Genre, Genre_film_work, Person, Person_film_work
from psycopg2.extensions import adapt, register_adapter, AsIs
import logging
import psycopg2.extras


logging.basicConfig(level=logging.INFO)


class PostgresSaver:

    def __init__(self, ps_connect):
        self.connect = ps_connect

    def save_all_data(self, data):
        cur = self.connect.cursor()
        query = 'INSERT INTO content.film_work(title, description, certificate, file_path, rating, type, created_at, updated_at, creation_date, id) VALUES (%s)'
        psycopg2.extras.execute_batch(cur, query, data.film_work)
       # cur.execute("""'PREPARE film_work_pln
         #   (film_work) AS
         #   INSERT INTO content.film_work
         #   VALUES(%s)
         #   ON CONFLICT (id) DO NOTHING;'""", data.film_work)


class Data:
    def __init__(
        self,
        film_work,
        genre,
        genre_film_work,
        person,
        person_film_work
    ):
        self.film_work = film_work
        self.genre = genre
        self.genre_film_work = genre_film_work
        self.person = person
        self.person_film_work = person_film_work


class SQLiteLoader:

    def __init__(self, lite_connect):
        self.connect = lite_connect

    def load_movies(self):
        cur = self.connect.cursor()
        film_work_cont = self.load_film_work(cur)
        genre_cont = self.load_genre(cur)
        genre_film_work_cont = self.load_genre_film_work(cur)
        person_cont = self.load_person(cur)
        person_film_work_cont = self.load_person_film_work(cur)
        return Data(
            film_work_cont,
            genre_cont,
            genre_film_work_cont,
            person_cont,
            person_film_work_cont)

    def load_film_work(self, cursor):
        logging.info('Start getting film_work data from sqlite_db')
        cursor.execute("SELECT * from film_work")
        row = cursor.fetchall()
        film_work_list = []
        for line in row:
            film_work_list.append(Film_work(
                title=line[1],
                description=line[2],
                certificate=line[4],
                file_path=line[5],
                rating=line[6],
                type=line[7],
                created_at=line[8],
                updated_at=line[9],
                creation_date=line[3],
                id=line[0]))
        logging.info('film_work data sucessfully stored')
        return film_work_list

    def load_genre(self, cursor):
        logging.info('Start getting genre data from sqlite_db')
        cursor.execute("SELECT * from genre")
        row = cursor.fetchall()
        genre_list = []
        for line in row:
            genre_list.append(Genre(
                name=line[1],
                description=line[2],
                created_at=line[3],
                updated_at=line[4],
                id=line[0]
            ))
        logging.info('genre data sucessfully stored')
        return genre_list

    def load_genre_film_work(self, cursor):
        logging.info('Start getting genre_film_work data from sqlite_db')
        cursor.execute("SELECT * from genre_film_work")
        row = cursor.fetchall()
        genre_film_work_list = []
        for line in row:
            genre_film_work_list.append(Genre_film_work(
                created_at=line[3],
                id=line[0]
            ))
        logging.info('genre_film_work data sucessfully stored')
        return genre_film_work_list

    def load_person(self, cursor):
        logging.info('Start getting person data from sqlite_db')
        cursor.execute("SELECT * from person")
        row = cursor.fetchall()
        person_list = []
        for line in row:
            person_list.append(Person(
                full_name=line[1],
                birth_date=line[2],
                created_at=line[3],
                updated_at=line[4],
                id=line[0]
            ))
        logging.info('person data sucessfully stored')
        return person_list

    def load_person_film_work(self, cursor):
        logging.info('Start getting person_film_work data from sqlite_db')
        cursor.execute("SELECT * from person_film_work")
        row = cursor.fetchall()
        person_film_work_list = []
        for line in row:
            person_film_work_list.append(Person_film_work(
                role=line[3],
                created_at=line[4],
                id=line[0]
            ))
        logging.info('person_film_work data sucessfully stored')
        return person_film_work_list
