from fastapi.testclient import TestClient

from main import app, get_url_shortener_service
from services import URLShortenerService
from storage import InMemoryURLRepository


test_repository = InMemoryURLRepository()
test_service = URLShortenerService(test_repository)


def get_test_url_shortener_service():
    return test_service


app.dependency_overrides[get_url_shortener_service] = get_test_url_shortener_service

client = TestClient(app)


def test_shorten_url():
    response = client.post(
        "/shorten",
        json={"url": "https://www.google.com"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "short_url" in data
    assert "short_code" in data


def test_redirect_to_original_url():
    shorten_response = client.post(
        "/shorten",
        json={"url": "https://www.google.com"}
    )

    short_code = shorten_response.json()["short_code"]

    redirect_response = client.get(
        f"/{short_code}",
        follow_redirects=False
    )

    assert redirect_response.status_code in [307, 308]
    assert redirect_response.headers["location"] == "https://www.google.com/"


def test_missing_short_code_returns_404():
    response = client.get("/missing-code")

    assert response.status_code == 404


def test_stats_endpoint_returns_url_stats():
    shorten_response = client.post(
        "/shorten",
        json={"url": "https://www.google.com"}
    )

    short_code = shorten_response.json()["short_code"]

    stats_response = client.get(f"/stats/{short_code}")

    assert stats_response.status_code == 200

    data = stats_response.json()

    assert data["short_code"] == short_code
    assert data["original_url"] == "https://www.google.com/"
    assert data["click_count"] == 0
    assert "created_at" in data


def test_stats_click_count_increases_after_redirect():
    shorten_response = client.post(
        "/shorten",
        json={"url": "https://www.google.com"}
    )

    short_code = shorten_response.json()["short_code"]

    client.get(f"/{short_code}", follow_redirects=False)
    client.get(f"/{short_code}", follow_redirects=False)

    stats_response = client.get(f"/stats/{short_code}")
    data = stats_response.json()

    assert data["click_count"] == 2


def test_stats_for_missing_short_code_returns_404():
    response = client.get("/stats/missing-code")

    assert response.status_code == 404