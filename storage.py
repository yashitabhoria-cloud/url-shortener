from datetime import datetime
from typing import Optional, Dict, Any

from interfaces import URLRepository


class InMemoryURLRepository(URLRepository):
    def __init__(self):
        self.urls = {}

    def save_url(self, short_code: str, original_url: str) -> None:
        self.urls[short_code] = {
            "original_url": original_url,
            "click_count": 0,
            "created_at": datetime.utcnow().isoformat()
        }

    def get_url(self, short_code: str) -> Optional[str]:
        url_data = self.urls.get(short_code)

        if url_data is None:
            return None

        return url_data["original_url"]

    def increment_click_count(self, short_code: str) -> None:
        if short_code in self.urls:
            self.urls[short_code]["click_count"] += 1

    def get_url_stats(self, short_code: str) -> Optional[Dict[str, Any]]:
        url_data = self.urls.get(short_code)

        if url_data is None:
            return None

        return {
            "short_code": short_code,
            "original_url": url_data["original_url"],
            "click_count": url_data["click_count"],
            "created_at": url_data["created_at"]
        }