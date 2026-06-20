from datetime import datetime
from typing import Optional, Dict, Any

from interfaces import URLRepository
from database import get_connection


class SQLiteURLRepository(URLRepository):
    def save_url(self, short_code: str, original_url: str) -> None:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO urls (short_code, original_url, click_count, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (short_code, original_url, 0, datetime.utcnow().isoformat())
        )

        connection.commit()
        connection.close()

    def get_url(self, short_code: str) -> Optional[str]:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT original_url FROM urls WHERE short_code = ?",
            (short_code,)
        )

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return None

        return row[0]

    def increment_click_count(self, short_code: str) -> None:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE urls
            SET click_count = click_count + 1
            WHERE short_code = ?
            """,
            (short_code,)
        )

        connection.commit()
        connection.close()

    def get_url_stats(self, short_code: str) -> Optional[Dict[str, Any]]:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT short_code, original_url, click_count, created_at
            FROM urls
            WHERE short_code = ?
            """,
            (short_code,)
        )

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return None

        return {
            "short_code": row[0],
            "original_url": row[1],
            "click_count": row[2],
            "created_at": row[3]
        }