from sqlite3.dbapi2 import Cursor
from typing import Any
import sqlite3

connection = sqlite3.connect("data.db")
# Cursor return rows as dictionary, but slower
# connection.row_factory = sqlite3.Row

def create_table():
    try:
        with connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS entries (content TEXT, date TEXT);"
            )
    except sqlite3.OperationalError as e:
        print(str(e))


def add_entry(entry_content: Any, entry_date: Any):
    with connection:
        connection.execute(
            "INSERT INTO entries (content, date) VALUES (?, ?);", (entry_content, entry_date)
        )


def get_entries() -> Cursor:
    cursor:Cursor = connection.execute(f"SELECT date, content FROM entries;")
    return cursor
