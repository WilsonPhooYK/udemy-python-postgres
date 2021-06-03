import os
from contextlib import contextmanager
from typing import cast
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

from typings.psycopg2 import SimpleConnectionPool as SimpleConnectionPoolType

DATABASE_PROMPT = "Enter the DATABASE_URI value or leave empty to load from .env file: "
database_uri = input(DATABASE_PROMPT)
if not database_uri:
    load_dotenv()
    database_uri = os.environ.get("DATABASE_URI")

pool:SimpleConnectionPoolType = cast(SimpleConnectionPoolType, SimpleConnectionPool(minconn=1, maxconn=10, dsn=database_uri))


@contextmanager
def get_connection():
    connection = pool.getconn()
    
    try:
        yield connection
    finally:
        pool.putconn(connection)