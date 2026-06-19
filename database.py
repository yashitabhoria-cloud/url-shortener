import sqlite3
from pathlib import Path


DATABASE_PATH = Path("urls.db")


def get_connection():
    """
    Opens a connection to the SQLite database file.

    If urls.db does not exist yet, SQLite will create it.
    """
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """
    Creates the database table if it does not already exist.
    """
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                short_code TEXT PRIMARY KEY,
                original_url TEXT NOT NULL
            )
            """
        )

        connection.commit()

    finally:
        connection.close()