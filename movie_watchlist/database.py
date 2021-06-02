import datetime
import sqlite3

# title, release_date, watched

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
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

SET_FOREIGN_KEY_SQLITE = "PRAGMA foreign_keys = ON;"
INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?);"
INSERT_USER = "INSERT INTO users (username) VALUES (?);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"

SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = """SELECT movies.* FROM movies
JOIN watched on movies.id = watched.movie_id
JOIN users on users.username = watched.user_username
WHERE users.username = ?;"""
SELECT_WATCHED_MOVIES_V2 = """SELECT movies.* FROM movies
JOIN (SELECT * FROM watched WHERE user_username = ?) a
ON movies.id = a.movie_id;"""
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES (?, ?);"
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?;"
SEARCH_MOVIE = "SELECT * FROM movies WHERE title LIKE ?;"
CREATE_RELEASE_INDEX = "CREATE INDEX IF NOT EXISTS idx_movies_release ON movies(release_timestamp);"


connection = sqlite3.connect("data.db")

def create_tables():
    with connection:
        connection.execute(SET_FOREIGN_KEY_SQLITE)
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)
        connection.execute(CREATE_RELEASE_INDEX)
        
def add_user(username: str):
    with connection:
        connection.execute(INSERT_USER, (username, ))

def add_movie(title: str, release_timestamp: float):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))

def get_movies(upcoming:bool = False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)
            
        return cursor.fetchall()

def search_movies(search_term: str):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SEARCH_MOVIE, (f"%{search_term}%",))
        return cursor.fetchall()

def watch_movie(username:str, movie_id: str):
    with connection:
        # connection.execute(DELETE_MOVIE, (title,))
        connection.execute(INSERT_WATCHED_MOVIE, (username, movie_id))

def get_watched_movies(username: str):
    cursor = connection.execute(SELECT_WATCHED_MOVIES_V2, (username,))
    return cursor.fetchall()
