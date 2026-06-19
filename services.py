from interfaces import URLRepository
from utils import generate_short_code


class URLShortenerService:
    def __init__(self, repository: URLRepository):
        self.repository = repository

    def create_short_url(self, original_url: str) -> str:
        short_code = generate_short_code()

        while self.repository.short_code_exists(short_code):
            short_code = generate_short_code()

        self.repository.save_url(short_code, original_url)

        return short_code

    def get_original_url(self, short_code: str) -> str | None:
        return self.repository.get_url(short_code)