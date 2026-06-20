import re
from typing import Optional, Dict, Any

from interfaces import URLRepository
from utils import generate_short_code


class InvalidShortCodeError(Exception):
    pass


class ShortCodeAlreadyExistsError(Exception):
    pass


class URLShortenerService:
    def __init__(self, repository: URLRepository):
        self.repository = repository

    def create_short_url(self, original_url: str, custom_code: str | None = None) -> str:
        if custom_code:
            custom_code = custom_code.strip()

            self._validate_custom_code(custom_code)

            existing_url = self.repository.get_url(custom_code)
            if existing_url is not None:
                raise ShortCodeAlreadyExistsError(
                    "This custom short code is already in use."
                )

            self.repository.save_url(custom_code, original_url)
            return custom_code

        short_code = self._generate_unique_short_code()
        self.repository.save_url(short_code, original_url)
        return short_code

    def _generate_unique_short_code(self) -> str:
        while True:
            short_code = generate_short_code()

            existing_url = self.repository.get_url(short_code)
            if existing_url is None:
                return short_code

    def _validate_custom_code(self, custom_code: str) -> None:
        reserved_words = {"shorten", "stats", "docs", "redoc", "openapi.json"}

        if custom_code in reserved_words:
            raise InvalidShortCodeError(
                "This short code is reserved and cannot be used."
            )

        pattern = r"^[a-zA-Z0-9_-]+$"

        if not re.match(pattern, custom_code):
            raise InvalidShortCodeError(
                "Custom short code can only contain letters, numbers, hyphens, and underscores."
            )

    def get_original_url(self, short_code: str) -> Optional[str]:
        return self.repository.get_url(short_code)

    def record_click(self, short_code: str) -> None:
        self.repository.increment_click_count(short_code)

    def get_stats(self, short_code: str) -> Optional[Dict[str, Any]]:
        return self.repository.get_url_stats(short_code)