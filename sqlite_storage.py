import sqlite3
from typing import Optional

from database import DATABASE_NAME
from interfaces import URLRepository


class SQLiteURLRepository(URLRepository):
    def __init__(self, database_name: str = DATABASE_NAME):
        self.database_name = database_name

    def save_url(
        self,
        short_code: str,
        original_url: str,
        created_at: str,
        expires_at: Optional[str] = None,
    ) -> None:
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO urls (short_code, original_url, clicks, created_at, expires_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (short_code, original_url, 0, created_at, expires_at),
        )

        connection.commit()
        connection.close()

    def get_original_url(self, short_code: str) -> Optional[str]:
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT original_url
            FROM urls
            WHERE short_code = ?
            """,
            (short_code,),
        )

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return None

        return row[0]

    def short_code_exists(self, short_code: str) -> bool:
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM urls
            WHERE short_code = ?
            """,
            (short_code,),
        )

        row = cursor.fetchone()
        connection.close()

        return row is not None

    def increment_clicks(self, short_code: str) -> None:
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE urls
            SET clicks = clicks + 1
            WHERE short_code = ?
            """,
            (short_code,),
        )

        connection.commit()
        connection.close()

    def get_url_stats(self, short_code: str) -> Optional[dict]:
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT short_code, original_url, clicks, created_at, expires_at
            FROM urls
            WHERE short_code = ?
            """,
            (short_code,),
        )

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return None

        return {
            "short_code": row[0],
            "original_url": row[1],
            "click_count": row[2],
            "created_at": row[3],
            "expires_at": row[4],
        }