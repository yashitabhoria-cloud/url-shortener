from fastapi.testclient import TestClient

from main import app, get_url_shortener_service
from storage import InMemoryURLRepository
from services import URLShortenerService


def create_test_service():
    repository = InMemoryURLRepository()
    return URLShortenerService(repository)


def test_shorten_url_returns_short_url():
    test_service = create_test_service()

    app.dependency_overrides[get_url_shortener_service] = lambda: test_service

    client = TestClient(app)

    response = client.post(
        "/shorten",
        json={"url": "https://www.google.com"},
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert "short_url" in data
    assert data["short_url"].startswith("http://testserver/")


def test_redirect_short_url():
    test_service = create_test_service()

    app.dependency_overrides[get_url_shortener_service] = lambda: test_service

    client = TestClient(app)

    shorten_response = client.post(
        "/shorten",
        json={"url": "https://www.google.com"},
    )

    short_url = shorten_response.json()["short_url"]
    short_code = short_url.split("/")[-1]

    redirect_response = client.get(
        f"/{short_code}",
        follow_redirects=False,
    )

    app.dependency_overrides.clear()

    assert redirect_response.status_code in [302, 307]
    assert redirect_response.headers["location"] == "https://www.google.com/"


def test_redirect_missing_short_code_returns_404():
    test_service = create_test_service()

    app.dependency_overrides[get_url_shortener_service] = lambda: test_service

    client = TestClient(app)

    response = client.get("/missingcode")

    app.dependency_overrides.clear()

    assert response.status_code == 404