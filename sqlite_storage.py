from interfaces import URLRepository
from database import get_connection


class SQLiteURLRepository(URLRepository):
    """
    SQLite implementation of URLRepository.

    This saves URLs into the urls.db database file.
    """

    def save_url(self, short_code: str, original_url: str) -> None:
        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO urls (short_code, original_url)
                VALUES (?, ?)
                """,
                (short_code, original_url),
            )

            connection.commit()

        finally:
            connection.close()

    def get_url(self, short_code: str) -> str | None:
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                SELECT original_url
                FROM urls
                WHERE short_code = ?
                """,
                (short_code,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return row["original_url"]

        finally:
            connection.close()

    def short_code_exists(self, short_code: str) -> bool:
        original_url = self.get_url(short_code)

        return original_url is not None