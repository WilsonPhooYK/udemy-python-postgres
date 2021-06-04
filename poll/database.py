from typing import cast
from psycopg2.extras import execute_values
from typings.psycopg2 import Connection

Poll = tuple[int, str, str]
Vote = tuple[str, int]
PollWithOption = tuple[int, str, str, str, int]
PollResults = tuple[int, str, int, float]

CREATE_POLLS = """CREATE TABLE IF NOT EXISTS polls
(id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"""
CREATE_OPTIONS = """CREATE TABLE IF NOT EXISTS options
(id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER);"""
CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes
(username TEXT, option_id INTEGER);"""


SELECT_ALL_POLLS = "SELECT * FROM polls;"
SELECT_POLL_WITH_OPTIONS = """SELECT * FROM polls
JOIN options ON polls.id = options.poll_id
WHERE polls.id = %s;"""
SELECT_LATEST_POLL = """SELECT * FROM polls
JOIN options ON polls.id = options.poll_id
WHERE polls.id = (
  SELECT id FROM polls ORDER BY id DESC LIMIT 1  
);"""
SELECT_LATEST_POLL_V2 = """WITH latest_id AS (
    SELECT id FROM polls ORDER BY id DESC LIMIT 1  
)

SELECT * FROM polls
JOIN options ON polls.id = options.poll_id
WHERE polls.id = (SELECT * FROM latest_id);"""
SELECT_POLL_VOTE_DETAILS = """SELECT
	options.id,
	options.option_text,
	COUNT(options.id) AS vote_count,
	COUNT(options.id) / SUM(COUNT(options.id)) OVER() * 100.0 AS vote_percentage
FROM options
LEFT JOIN votes ON votes.option_id = options.id
WHERE options.poll_id = %s
GROUP BY options.id;"""
SELECT_POLL_VOTE_DETAILS_V2 = """SELECT
	options.id,
	options.option_text,
	COALESCE(A.vote_count, 0) AS vote_count,
	COALESCE(A.vote_percentage, 0.0) AS vote_percentage
FROM options
LEFT JOIN (
	SELECT
		options.id,
		options.option_text,
		COUNT(options.id) AS vote_count,
		COUNT(options.id) / SUM(COUNT(options.id)) OVER() * 100.0 AS vote_percentage
	FROM options
	INNER JOIN votes ON votes.option_id = options.id
	WHERE options.poll_id = %s
	GROUP BY options.id
) AS A
ON options.id = A.id
WHERE options.poll_id = %s;"""
SELECT_RANDOM_VOTE = "SELECT * FROM votes WHERE option_id = %s ORDER BY RANDOM() LIMIT 1;"

INSERT_POLL_RETURN_ID = "INSERT INTO polls (title, owner_username) VALUES (%s, %s) RETURNING id;"
INSERT_OPTION = "INSERT INTO options (option_text, poll_id) VALUES %s;"
INSERT_VOTE = "INSERT INTO votes (username, option_id) VALUES (%s, %s);"



def create_tables(connection: Connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_POLLS)
            cursor.execute(CREATE_OPTIONS)
            cursor.execute(CREATE_VOTES)


def get_polls(connection: Connection) -> list[Poll]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_POLLS)
            return cast(list[Poll], cursor.fetchall())


def get_latest_poll(connection: Connection) -> list[PollWithOption]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_LATEST_POLL)
            return cast(list[PollWithOption], cursor.fetchall())


def get_poll_details(connection: Connection, poll_id: int) -> list[PollWithOption]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POLL_WITH_OPTIONS, (poll_id,))
            return cast(list[PollWithOption], cursor.fetchall())


def get_poll_and_vote_results(connection: Connection, poll_id: int) -> list[PollResults]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POLL_VOTE_DETAILS, (poll_id,))
            return cast(list[PollResults], cursor.fetchall())


def get_random_poll_vote(connection: Connection, option_id: int) -> Vote:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_RANDOM_VOTE, (option_id,))
            return cast(Vote, cursor.fetchone())


def create_poll(connection: Connection, title: str, owner: str, options: list[str]):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_POLL_RETURN_ID, (title, owner))
            # cursor.execute("SELECT FROM polls ORDER BY id DESC LIMIT 1;")
            
            poll_id = cursor.fetchone()[0]
            option_values = [(option_text, poll_id) for option_text in options]
            
            # for option in option_values:
            #     cursor.execute(INSERT_OPTION, option)
                
            execute_values(cursor, INSERT_OPTION, option_values)

def add_poll_vote(connection: Connection, username: str, option_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VOTE, (username, option_id))