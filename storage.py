from typing import Optional

from interfaces import URLRepository


class InMemoryURLRepository(URLRepository):
    def __init__(self):
        self.urls = {}

    def save_url(
        self,
        short_code: str,
        original_url: str,
        created_at: str,
        expires_at: Optional[str] = None,
    ) -> None:
        self.urls[short_code] = {
            "original_url": original_url,
            "clicks": 0,
            "created_at": created_at,
            "expires_at": expires_at,
        }

    def get_original_url(self, short_code: str) -> Optional[str]:
        url_data = self.urls.get(short_code)

        if url_data is None:
            return None

        return url_data["original_url"]

    def short_code_exists(self, short_code: str) -> bool:
        return short_code in self.urls

    def increment_clicks(self, short_code: str) -> None:
        if short_code in self.urls:
            self.urls[short_code]["clicks"] += 1

    def get_url_stats(self, short_code: str) -> Optional[dict]:
        url_data = self.urls.get(short_code)

        if url_data is None:
            return None

        return {
            "short_code": short_code,
            "original_url": url_data["original_url"],
            "click_count": url_data["clicks"],
            "created_at": url_data["created_at"],
            "expires_at": url_data["expires_at"],
        }
    def delete(self, short_code: str) -> bool:
        if short_code not in self.urls:
            return False

        del self.urls[short_code]
        return True
    
    def update_original_url(self, short_code: str, original_url: str) -> bool:
        if short_code not in self.urls:
            return False

        self.urls[short_code]["original_url"] = original_url
        return True
    
    def list_urls(self, limit: int, offset: int) -> list[dict]:
        all_urls = []

        for short_code, url_data in self.urls.items():
            all_urls.append({
                "short_code": short_code,
                **url_data,
            })

        all_urls.sort(key=lambda item: item["created_at"], reverse=True)

        return all_urls[offset:offset + limit]

    def count_urls(self) -> int:
        return len(self.urls)