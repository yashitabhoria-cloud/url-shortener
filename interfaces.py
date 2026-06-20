from abc import ABC, abstractmethod
from typing import Optional


class URLRepository(ABC):
    @abstractmethod
    def save_url(
        self,
        short_code: str,
        original_url: str,
        created_at: str,
        expires_at: Optional[str] = None,
    ) -> None:
        pass

    @abstractmethod
    def get_original_url(self, short_code: str) -> Optional[str]:
        pass

    @abstractmethod
    def short_code_exists(self, short_code: str) -> bool:
        pass

    @abstractmethod
    def increment_clicks(self, short_code: str) -> None:
        pass

    @abstractmethod
    def get_url_stats(self, short_code: str) -> Optional[dict]:
        pass

    @abstractmethod
    def delete(self, short_code: str) -> bool:
        pass