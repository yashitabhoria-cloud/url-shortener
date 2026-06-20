from services import URLShortenerService
from storage import InMemoryURLRepository


def test_create_short_url_returns_code():
    repository = InMemoryURLRepository()
    service = URLShortenerService(repository)

    short_code = service.create_short_url("https://www.google.com")

    assert isinstance(short_code, str)
    assert len(short_code) > 0


def test_get_original_url_returns_saved_url():
    repository = InMemoryURLRepository()
    service = URLShortenerService(repository)

    short_code = service.create_short_url("https://www.google.com")
    original_url = service.get_original_url(short_code)

    assert original_url == "https://www.google.com"


def test_get_original_url_returns_none_for_missing_code():
    repository = InMemoryURLRepository()
    service = URLShortenerService(repository)

    original_url = service.get_original_url("missing-code")

    assert original_url is None


def test_click_count_starts_at_zero():
    repository = InMemoryURLRepository()
    service = URLShortenerService(repository)

    short_code = service.create_short_url("https://www.google.com")
    stats = service.get_stats(short_code)

    assert stats["click_count"] == 0


def test_record_click_increases_click_count():
    repository = InMemoryURLRepository()
    service = URLShortenerService(repository)

    short_code = service.create_short_url("https://www.google.com")

    service.record_click(short_code)
    service.record_click(short_code)

    stats = service.get_stats(short_code)

    assert stats["click_count"] == 2


def test_get_stats_returns_none_for_missing_code():
    repository = InMemoryURLRepository()
    service = URLShortenerService(repository)

    stats = service.get_stats("missing-code")

    assert stats is None