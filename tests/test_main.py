from fastapi.testclient import TestClient

from main import app, get_url_shortener_service
from services import URLShortenerService
from storage import InMemoryURLRepository
from datetime import datetime, timedelta, timezone

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

def test_create_custom_short_code():
    response = client.post(
        "/shorten",
        json={
            "url": "https://example.com",
            "custom_code": "example",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["short_code"] == "example"
    assert data["short_url"].endswith("/example")


def test_duplicate_custom_short_code_fails():
    first_response = client.post(
        "/shorten",
        json={
            "url": "https://example.com",
            "custom_code": "duplicate",
        },
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/shorten",
        json={
            "url": "https://google.com",
            "custom_code": "duplicate",
        },
    )

    assert second_response.status_code == 409


def test_invalid_custom_short_code_fails():
    response = client.post(
        "/shorten",
        json={
            "url": "https://example.com",
            "custom_code": "bad code",
        },
    )

    assert response.status_code == 400

def test_shorten_url_with_expiration():
    future_time = datetime.now(timezone.utc) + timedelta(days=1)

    response = client.post(
        "/shorten",
        json={
            "url": "https://example.com",
            "expires_at": future_time.isoformat(),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["short_code"] is not None
    assert data["short_url"] is not None
    assert data["expires_at"] is not None


def test_shorten_url_with_past_expiration_returns_400():
    past_time = datetime.now(timezone.utc) - timedelta(days=1)

    response = client.post(
        "/shorten",
        json={
            "url": "https://example.com",
            "expires_at": past_time.isoformat(),
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Expiration time must be in the future"


def test_stats_include_expiration_fields():
    future_time = datetime.now(timezone.utc) + timedelta(days=1)

    create_response = client.post(
        "/shorten",
        json={
            "url": "https://example.com",
            "expires_at": future_time.isoformat(),
        },
    )

    short_code = create_response.json()["short_code"]

    stats_response = client.get(f"/stats/{short_code}")

    assert stats_response.status_code == 200

    data = stats_response.json()

    assert data["expires_at"] is not None
    assert data["is_expired"] is False

def test_delete_existing_short_url():
    create_response = client.post(
        "/shorten",
        json={"url": "https://example.com"},
    )

    short_code = create_response.json()["short_code"]

    delete_response = client.delete(f"/{short_code}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/{short_code}")

    assert get_response.status_code == 404


def test_delete_missing_short_url_returns_404():
    response = client.delete("/doesnotexist")

    assert response.status_code == 404
    assert response.json()["detail"] == "Short code not found"


def test_stats_for_deleted_short_url_returns_404():
    create_response = client.post(
        "/shorten",
        json={"url": "https://example.com"},
    )

    short_code = create_response.json()["short_code"]

    client.delete(f"/{short_code}")

    stats_response = client.get(f"/stats/{short_code}")

    assert stats_response.status_code == 404

def test_update_existing_short_url():
    create_response = client.post(
        "/shorten",
        json={"url": "https://google.com"},
    )

    short_code = create_response.json()["short_code"]

    update_response = client.patch(
        f"/{short_code}",
        json={"url": "https://youtube.com"},
    )

    assert update_response.status_code == 204

    redirect_response = client.get(f"/{short_code}", follow_redirects=False)

    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://youtube.com/"

def test_update_missing_short_url_returns_404():
    response = client.patch(
        "/doesnotexist",
        json={"url": "https://youtube.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Short code not found"

def test_update_short_url_with_invalid_url_returns_422():
    create_response = client.post(
        "/shorten",
        json={"url": "https://google.com"},
    )

    short_code = create_response.json()["short_code"]

    response = client.patch(
        f"/{short_code}",
        json={"url": "not-a-valid-url"},
    )

    assert response.status_code == 422

def test_list_urls_returns_created_urls(client):
    client.post("/shorten", json={"url": "https://example.com"})
    client.post("/shorten", json={"url": "https://google.com"})

    response = client.get("/urls")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert data["limit"] == 10
    assert data["offset"] == 0
    assert len(data["items"]) == 2

    first_item = data["items"][0]

    assert "short_code" in first_item
    assert "original_url" in first_item
    assert "short_url" in first_item
    assert "click_count" in first_item
    assert "created_at" in first_item
    assert "expires_at" in first_item
    assert "is_expired" in first_item


def test_list_urls_supports_pagination(client):
    client.post("/shorten", json={"url": "https://example.com/1"})
    client.post("/shorten", json={"url": "https://example.com/2"})
    client.post("/shorten", json={"url": "https://example.com/3"})

    response = client.get("/urls?limit=1&offset=1")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 3
    assert data["limit"] == 1
    assert data["offset"] == 1
    assert len(data["items"]) == 1


def test_list_urls_rejects_invalid_limit(client):
    response = client.get("/urls?limit=0")

    assert response.status_code == 422


def test_list_urls_rejects_invalid_offset(client):
    response = client.get("/urls?offset=-1")

    assert response.status_code == 422