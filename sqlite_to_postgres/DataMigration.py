from Dataclasses import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
import logging
from psycopg2.extras import execute_batch
import dataclasses


logging.basicConfig(level=logging.INFO)


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


class PostgresSaver:

    def __init__(self, ps_connect):
        self.connect = ps_connect

    def save_all_data(self, data):
        cur = self.connect.cursor()
        self.save_film_work(data, cur)
        self.save_genre(data, cur)
        self.save_genre_film_work(data, cur)
        self.save_person(data, cur)
        self.save_person_film_work(data, cur)
    
    def save_film_work(self, data, cursor):
        query = """INSERT INTO content.film_work (title, description, creation_date, certificate, file_path, rating, type, created_at, updated_at, id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING"""
        try:
            execute_batch(cursor, query, data.film_work)
        except:
            logging.exception('message')

    def save_genre(self, data, cursor):
        query = """INSERT INTO content.genre (name, description, created_at, updated_at, id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING"""
        try:
            execute_batch(cursor, query, data.genre)
        except:
            logging.exception('message')

    def save_genre_film_work(self, data, cursor):
        query = """INSERT INTO content.genre_film_work (created_at, id, film_work_id, genre_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING"""
        try:
            execute_batch(cursor, query, data.genre_film_work)
        except:
            logging.exception('message')

    def save_person(self, data, cursor):
        query = """INSERT INTO content.person (full_name, birth_date, created_at, updated_at, id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING"""
        try:
            execute_batch(cursor, query, data.person)
        except:
            logging.exception('message')
    
    def save_person_film_work(self, data, cursor):
        query = """INSERT INTO content.person_film_work (role, created_at, id, film_work_id, person_id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING"""
        try:
            execute_batch(cursor, query, data.person_film_work)
        except:
            logging.exception('message')


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
        cursor.execute("SELECT title, description, creation_date, certificate, file_path, rating, type, created_at, updated_at, id from film_work")
        row = cursor.fetchall()
        film_work_list = []
        for line in row:
            film_work_list.append(dataclasses.astuple(FilmWork(*line)))
        logging.info('film_work data sucessfully stored')
        return film_work_list

    def load_genre(self, cursor):
        logging.info('Start getting genre data from sqlite_db')
        cursor.execute("SELECT name, description, created_at, updated_at, id from genre")
        row = cursor.fetchall()
        genre_list = []
        for line in row:
            genre_list.append(dataclasses.astuple(Genre(*line)))
        logging.info('genre data sucessfully stored')
        return genre_list

    def load_genre_film_work(self, cursor):
        logging.info('Start getting genre_film_work data from sqlite_db')
        cursor.execute("SELECT created_at, id, film_work_id, genre_id from genre_film_work")
        row = cursor.fetchall()
        genre_film_work_list = []
        for line in row:
            genre_film_work_list.append(dataclasses.astuple(GenreFilmWork(*line)))
        logging.info('genre_film_work data sucessfully stored')
        return genre_film_work_list

    def load_person(self, cursor):
        logging.info('Start getting person data from sqlite_db')
        cursor.execute("SELECT full_name, birth_date, created_at, updated_at, id from person")
        row = cursor.fetchall()
        person_list = []
        for line in row:
            person_list.append(dataclasses.astuple(Person(*line)))
        logging.info('person data sucessfully stored')
        return person_list

    def load_person_film_work(self, cursor):
        logging.info('Start getting person_film_work data from sqlite_db')
        cursor.execute("SELECT role, created_at, id, film_work_id, person_id from person_film_work")
        row = cursor.fetchall()
        person_film_work_list = []
        for line in row:
            person_film_work_list.append(dataclasses.astuple(PersonFilmWork(*line)))
        logging.info('person_film_work data sucessfully stored')
        return person_film_work_list
