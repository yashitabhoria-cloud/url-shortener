from storage import InMemoryURLRepository
from services import URLShortenerService


def test_create_short_url_saves_original_url():
    repository = InMemoryURLRepository()
    service = URLShortenerService(repository)

    original_url = "https://www.google.com"

    short_code = service.create_short_url(original_url)

    saved_url = service.get_original_url(short_code)

    assert saved_url == original_url


def test_get_original_url_returns_saved_url():
    repository = InMemoryURLRepository()
    service = URLShortenerService(repository)

    original_url = "https://www.google.com"
    short_code = service.create_short_url(original_url)

    result = service.get_original_url(short_code)

    assert result == original_url


def test_get_original_url_returns_none_for_missing_code():
    repository = InMemoryURLRepository()
    service = URLShortenerService(repository)

    result = service.get_original_url("doesnotexist")

    assert result is None