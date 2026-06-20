from services import URLShortenerService
from storage import InMemoryURLRepository
from datetime import datetime, timedelta, timezone

import pytest
from services import ExpiredShortCodeError, InvalidExpirationError
from storage import InMemoryURLRepository
from services import URLShortenerService

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

def test_create_short_url_with_future_expiration():
    repository = InMemoryURLRepository()
    service = URLShortenerService(repository)

    future_time = datetime.now(timezone.utc) + timedelta(days=1)

    short_code = service.create_short_url(
        "https://example.com",
        expires_at=future_time,
    )

    stats = service.get_url_stats(short_code)

    assert stats is not None
    assert stats["expires_at"] is not None
    assert stats["is_expired"] is False


def test_create_short_url_with_past_expiration_fails():
    repository = InMemoryURLRepository()
    service = URLShortenerService(repository)

    past_time = datetime.now(timezone.utc) - timedelta(days=1)

    with pytest.raises(InvalidExpirationError):
        service.create_short_url(
            "https://example.com",
            expires_at=past_time,
        )


def test_expired_short_url_cannot_redirect():
    repository = InMemoryURLRepository()
    service = URLShortenerService(repository)

    created_at = datetime.now(timezone.utc).isoformat()
    expired_at = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()

    repository.save_url(
        "expired123",
        "https://example.com",
        created_at,
        expired_at,
    )

    with pytest.raises(ExpiredShortCodeError):
        service.get_original_url("expired123")