import sqlite3


DATABASE_NAME = "urls.db"


def initialize_database() -> None:
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS urls (
            short_code TEXT PRIMARY KEY,
            original_url TEXT NOT NULL,
            clicks INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            expires_at TEXT
        )
        """
    )

    cursor.execute("PRAGMA table_info(urls)")
    existing_columns = [column[1] for column in cursor.fetchall()]

    if "expires_at" not in existing_columns:
        cursor.execute("ALTER TABLE urls ADD COLUMN expires_at TEXT")

    connection.commit()
    connection.close()