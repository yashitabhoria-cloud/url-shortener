from datetime import datetime, timezone
from typing import Optional

from interfaces import URLRepository
from utils import generate_short_code, is_valid_custom_code


class InvalidShortCodeError(Exception):
    pass

class ShortCodeNotFoundError(Exception):
    pass

class ShortCodeAlreadyExistsError(Exception):
    pass


class InvalidExpirationError(Exception):
    pass


class ExpiredShortCodeError(Exception):
    pass


class URLShortenerService:
    def __init__(self, repository: URLRepository):
        self.repository = repository

    def record_click(self, short_code: str) -> None:
        self.repository.increment_clicks(short_code)


    def get_stats(self, short_code: str) -> Optional[dict]:
        return self.get_url_stats(short_code)

    def create_short_url(
        self,
        original_url: str,
        custom_code: Optional[str] = None,
        expires_at: Optional[datetime] = None,
    ) -> str:
        created_at = datetime.now(timezone.utc).isoformat()
        expires_at_string = self._normalize_expiration(expires_at)

        if custom_code is not None:
            if not is_valid_custom_code(custom_code):
                raise InvalidShortCodeError()

            if self.repository.short_code_exists(custom_code):
                raise ShortCodeAlreadyExistsError()

            short_code = custom_code
        else:
            short_code = generate_short_code()

            while self.repository.short_code_exists(short_code):
                short_code = generate_short_code()

        self.repository.save_url(
            short_code,
            original_url,
            created_at,
            expires_at_string,
        )

        return short_code

    def get_original_url(self, short_code: str) -> Optional[str]:
        stats = self.repository.get_url_stats(short_code)

        if stats is None:
            return None

        if self._is_expired(stats.get("expires_at")):
            raise ExpiredShortCodeError()

        self.repository.increment_clicks(short_code)

        return stats["original_url"]

    def get_url_stats(self, short_code: str) -> Optional[dict]:
        stats = self.repository.get_url_stats(short_code)

        if stats is None:
            return None

        stats["is_expired"] = self._is_expired(stats.get("expires_at"))

        return stats

    def _normalize_expiration(self, expires_at: Optional[datetime]) -> Optional[str]:
        if expires_at is None:
            return None

        expiry_time = self._convert_to_utc_datetime(expires_at)

        if expiry_time <= datetime.now(timezone.utc):
            raise InvalidExpirationError()

        return expiry_time.isoformat()

    def _is_expired(self, expires_at: Optional[str]) -> bool:
        if expires_at is None:
            return False

        expiry_time = self._convert_to_utc_datetime(expires_at)

        return expiry_time <= datetime.now(timezone.utc)

    def _convert_to_utc_datetime(self, value) -> datetime:
        if isinstance(value, str):
            value = value.replace("Z", "+00:00")
            value = datetime.fromisoformat(value)

        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)
    
    def delete_short_url(self, short_code: str) -> None:
        was_deleted = self.repository.delete(short_code)

        if not was_deleted:
            raise ShortCodeNotFoundError()