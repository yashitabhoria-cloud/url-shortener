from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class URLRepository(ABC):
    @abstractmethod
    def save_url(self, short_code: str, original_url: str) -> None:
        pass

    @abstractmethod
    def get_url(self, short_code: str) -> Optional[str]:
        pass

    @abstractmethod
    def increment_click_count(self, short_code: str) -> None:
        pass

    @abstractmethod
    def get_url_stats(self, short_code: str) -> Optional[Dict[str, Any]]:
        pass