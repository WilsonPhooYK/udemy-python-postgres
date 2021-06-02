import os
import datetime
from typing import Any, Iterable
import psycopg2
import psycopg2.extras
from typings.psycopg2 import Connection

from dotenv import load_dotenv

load_dotenv()

# title, release_date, watched

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
  username TEXT PRIMARY KEY
);"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
  user_username TEXT,
  movie_id INTEGER,
  FOREIGN KEY(user_username) REFERENCES users(username),
  FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"
INSERT_USER = "INSERT INTO users (username) VALUES (%s);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = %s;"

SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"
SELECT_WATCHED_MOVIES = """SELECT movies.* FROM movies
JOIN watched on movies.id = watched.movie_id
JOIN users on users.username = watched.user_username
WHERE users.username = %s;"""
SELECT_WATCHED_MOVIES_V2 = """SELECT movies.* FROM movies
JOIN (SELECT * FROM watched WHERE user_username = %s) a
ON movies.id = a.movie_id;"""
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES (%s, %s);"
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = %s;"
SEARCH_MOVIE = "SELECT * FROM movies WHERE UPPER(title) LIKE UPPER(%s);"
CREATE_RELEASE_INDEX = "CREATE INDEX IF NOT EXISTS idx_movies_release ON movies(release_timestamp);"

connection: Connection = psycopg2.connect(os.environ["DATABASE_URL"]) # type: ignore

def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)
            cursor.execute(CREATE_RELEASE_INDEX)
        
def add_user(username: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username, ))

def add_movie(title: str, release_timestamp: float):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES, (title, release_timestamp))

def get_movies(upcoming:bool = False)  -> Iterable[Any]:
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                today_timestamp = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)
                
            return cursor.fetchall()

def search_movies(search_term: str) -> Iterable[Any]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_MOVIE, (f"%{search_term}%",))
            return cursor.fetchall()

def watch_movie(username:str, movie_id: str):
    with connection:
        with connection.cursor() as cursor:
            # cursor.execute(DELETE_MOVIE, (title,))
            cursor.execute(INSERT_WATCHED_MOVIE, (username, movie_id))
            

def get_watched_movies(username: str) -> Iterable[Any]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES_V2, (username,))
            return cursor.fetchall()
