from typing import Optional, Dict, Any

from interfaces import URLRepository
from utils import generate_short_code


class URLShortenerService:
    def __init__(self, repository: URLRepository):
        self.repository = repository

    def create_short_url(self, original_url: str) -> str:
        short_code = generate_short_code()
        self.repository.save_url(short_code, original_url)
        return short_code

    def get_original_url(self, short_code: str) -> Optional[str]:
        return self.repository.get_url(short_code)

    def record_click(self, short_code: str) -> None:
        self.repository.increment_click_count(short_code)

    def get_stats(self, short_code: str) -> Optional[Dict[str, Any]]:
        return self.repository.get_url_stats(short_code)