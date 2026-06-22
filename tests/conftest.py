import pytest
from fastapi.testclient import TestClient

from main import app, get_url_shortener_service
from services import URLShortenerService
from storage import InMemoryURLRepository


@pytest.fixture
def client():
    test_repository = InMemoryURLRepository()
    test_service = URLShortenerService(test_repository)

    def override_get_url_shortener_service():
        return test_service

    app.dependency_overrides[get_url_shortener_service] = override_get_url_shortener_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()