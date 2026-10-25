import pytest
import requests

BASE = "https://jsonplaceholder.typicode.com"

pytestmark = pytest.mark.api


def test_list_posts_returns_100_items_with_expected_fields():
    r = requests.get(f"{BASE}/posts", timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 100
    assert {"userId", "id", "title", "body"} <= body[0].keys()


def test_get_single_post_matches_requested_id():
    r = requests.get(f"{BASE}/posts/7", timeout=10)
    assert r.status_code == 200
    assert r.json()["id"] == 7


def test_unknown_post_returns_404():
    assert requests.get(f"{BASE}/posts/99999", timeout=10).status_code == 404


def test_create_post_echoes_payload_and_assigns_id():
    payload = {"title": "qa", "body": "check", "userId": 1}
    r = requests.post(f"{BASE}/posts", json=payload, timeout=10)
    assert r.status_code == 201
    assert payload.items() <= r.json().items()
    assert "id" in r.json()


def test_filter_posts_by_user():
    r = requests.get(f"{BASE}/posts", params={"userId": 3}, timeout=10)
    assert r.status_code == 200
    assert r.json() and all(p["userId"] == 3 for p in r.json())
