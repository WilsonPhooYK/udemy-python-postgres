from typing import cast
from contextlib import contextmanager
from typings.psycopg2 import Connection

Poll = tuple[int, str, str]
Option = tuple[int, str, int]
Vote = tuple[str, int, float]
OptionSpread = tuple[str, int]

CREATE_POLLS = """CREATE TABLE IF NOT EXISTS polls
(id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"""
CREATE_OPTIONS = """CREATE TABLE IF NOT EXISTS options
(id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER, FOREIGN KEY(poll_id) REFERENCES polls (id));"""
CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes
(username TEXT, option_id INTEGER, vote_timestamp INTEGER, FOREIGN KEY(option_id) REFERENCES options (id));"""

SELECT_POLL = "SELECT * FROM polls WHERE id = %s;"
SELECT_ALL_POLLS = "SELECT * FROM polls;"
SELECT_POLL_OPTIONS = "SELECT * FROM options WHERE poll_id = %s;"
SELECT_POLL_WITH_OPTIONS = """SELECT * FROM polls
JOIN options ON polls.id = options.poll_id
WHERE polls.id = %s;"""
SELECT_LATEST_POLL = """SELECT * FROM polls
WHERE polls.id = (
  SELECT id FROM polls ORDER BY id DESC LIMIT 1  
);"""
SELECT_LATEST_POLL_V2 = """WITH latest_id AS (
    SELECT id FROM polls ORDER BY id DESC LIMIT 1  
)

SELECT * FROM polls
JOIN options ON polls.id = options.poll_id
WHERE polls.id = (SELECT * FROM latest_id);"""

SELECT_OPTION = "SELECT * FROM options WHERE id = %s;"
SELECT_VOTES_FOR_OPTION = "SELECT * FROM votes WHERE votes.option_id = %s;"
SELECT_OPTIONS_IN_POLL = """SELECT options.option_text, COUNT(votes)
FROM options
JOIN polls ON options.poll_id = polls.id
JOIN votes ON votes.option_id = options.id
WHERE polls.id = %s
GROUP BY options.option_text;"""
SELECT_POLLS_AND_VOTES = """SELECT polls.title, COUNT(votes.option_id)
FROM polls
JOIN options ON options.poll_id = polls.id
JOIN votes ON votes.option_id = options.id
GROUP BY polls.title
"""

INSERT_POLL_RETURN_ID = "INSERT INTO polls (title, owner_username) VALUES (%s, %s) RETURNING id;"
INSERT_OPTION_RETURNING_ID = "INSERT INTO options (option_text, poll_id) VALUES (%s, %s) RETURNING id;"
INSERT_VOTE = "INSERT INTO votes (username, option_id, vote_timestamp) VALUES (%s, %s, %s);"

@contextmanager
def get_cursor(connection: Connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


def create_tables(connection: Connection):
    with get_cursor(connection) as cursor:
        cursor.execute(CREATE_POLLS)
        cursor.execute(CREATE_OPTIONS)
        cursor.execute(CREATE_VOTES)
            
# -- polls --
def create_poll(connection: Connection, title: str, owner: str):
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_POLL_RETURN_ID, (title, owner))
        # cursor.execute("SELECT FROM polls ORDER BY id DESC LIMIT 1;")
        
        poll_id = cursor.fetchone()[0]
        return poll_id


def get_polls(connection: Connection) -> list[Poll]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_POLLS)
        return cast(list[Poll], cursor.fetchall())


def get_poll(connection: Connection, poll_id: int) -> Poll:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POLL, (poll_id, ))
        return cast(Poll, cursor.fetchone())


def get_latest_poll(connection: Connection) -> Poll:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_LATEST_POLL)
        return cast(Poll, cursor.fetchone())


def get_poll_options(connection: Connection, poll_id: int) -> list[Option]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POLL_OPTIONS, (poll_id,))
        return cast(list[Option], cursor.fetchall())
    
def get_options_spread_in_poll(connection: Connection, poll_id: int) -> list[OptionSpread]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_OPTIONS_IN_POLL, (poll_id,))
        return cast(list[OptionSpread], cursor.fetchall())
    
def get_polls_and_votes(connection: Connection) -> list[OptionSpread]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POLLS_AND_VOTES)
        return cast(list[OptionSpread], cursor.fetchall())
# -- options --

def get_option(connection: Connection, option_id: int) -> Option:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_OPTION, (option_id, ))
        return cast(Option, cursor.fetchone())

def add_option(connection: Connection, option_text: str,  poll_id: int) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_OPTION_RETURNING_ID, (option_text, poll_id))
        option_id = cursor.fetchone()[0]
        return option_id

# -- votes --

def get_votes_for_option(connection: Connection, option_id: int) -> list[Vote]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_VOTES_FOR_OPTION, (option_id, ))
        return cast(list[Vote], cursor.fetchall())

def add_poll_vote(connection: Connection, username: str, vote_timestamp: float, option_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_VOTE, (username, option_id, vote_timestamp))
