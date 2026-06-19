from interfaces import URLRepository


class InMemoryURLRepository(URLRepository):
    def __init__(self):
        self.urls: dict[str, str] = {}

    def save_url(self, short_code: str, original_url: str) -> None:
        self.urls[short_code] = original_url

    def get_url(self, short_code: str) -> str | None:
        return self.urls.get(short_code)

    def short_code_exists(self, short_code: str) -> bool:
        return short_code in self.urls