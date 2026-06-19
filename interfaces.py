from abc import ABC, abstractmethod


class URLRepository(ABC):
    @abstractmethod
    def save_url(self, short_code: str, original_url: str) -> None:
        pass

    @abstractmethod
    def get_url(self, short_code: str) -> str | None:
        pass

    @abstractmethod
    def short_code_exists(self, short_code: str) -> bool:
        pass