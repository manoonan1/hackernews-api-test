import pytest
import requests


BASE_URL = "https://hacker-news.firebaseio.com/v0"
HTTP_BASE_URL = "http://hacker-news.firebaseio.com/v0"


@pytest.mark.security
def test_http_connection_rejected():
    """API rejects HTTP connections - only HTTPS is supported."""
    with pytest.raises(requests.exceptions.ConnectionError):
        requests.get(f"{HTTP_BASE_URL}/topstories.json", timeout=5)


@pytest.mark.security
def test_empty_item_id_returns_401():
    """API returns 401 for empty item ID."""
    response = requests.get(f"{BASE_URL}/item/.json")

    assert response.status_code == 401
    assert response.json()["error"] == "Permission denied"


@pytest.mark.security
def test_invalid_endpoint_returns_401():
    """API returns 401 for invalid endpoint (items instead of item)."""
    response = requests.get(f"{BASE_URL}/items.json")

    assert response.status_code == 401
    assert response.json()["error"] == "Permission denied"
