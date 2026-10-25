import time

import pytest
import requests
from jsonschema import validate

BASE = "https://jsonplaceholder.typicode.com"
MAX_SECONDS = 2.0  # response-time threshold from the QA Master Guide, Playbook B

POST_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title", "body"],
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
}

pytestmark = pytest.mark.api


def timed_get(path: str, **kwargs):
    start = time.perf_counter()
    r = requests.get(f"{BASE}{path}", timeout=10, **kwargs)
    return r, time.perf_counter() - start


def test_post_matches_json_schema():
    r, _ = timed_get("/posts/1")
    assert r.headers["Content-Type"].startswith("application/json")
    validate(r.json(), POST_SCHEMA)


def test_every_listed_post_matches_schema():
    r, _ = timed_get("/posts")
    for post in r.json():
        validate(post, POST_SCHEMA)


@pytest.mark.performance
@pytest.mark.parametrize("path", ["/posts", "/posts/1", "/users"])
def test_read_endpoints_respond_within_threshold(path):
    r, elapsed = timed_get(path)
    assert r.status_code == 200
    assert elapsed < MAX_SECONDS, f"{path} took {elapsed:.2f}s"


def test_chained_flow_create_read_comments_of_a_user_post():
    """One request feeds the next (Playbook B: chain, don't isolate)."""
    posts, _ = timed_get("/posts", params={"userId": 2})
    first_id = posts.json()[0]["id"]
    post, _ = timed_get(f"/posts/{first_id}")
    assert post.json()["userId"] == 2
    comments, _ = timed_get(f"/posts/{first_id}/comments")
    assert comments.status_code == 200
    assert all(c["postId"] == first_id for c in comments.json())


def test_update_and_delete_respond_successfully():
    put = requests.put(f"{BASE}/posts/1", json={"id": 1, "title": "t", "body": "b", "userId": 1}, timeout=10)
    assert put.status_code == 200
    assert put.json()["title"] == "t"
    assert requests.delete(f"{BASE}/posts/1", timeout=10).status_code == 200


@pytest.mark.negative
@pytest.mark.parametrize("post_id", ["abc", "-1", "0"])
def test_invalid_post_ids_do_not_return_a_post(post_id):
    r, _ = timed_get(f"/posts/{post_id}")
    assert r.status_code == 404


@pytest.mark.negative
@pytest.mark.security
def test_oversized_payload_does_not_crash_the_server():
    payload = {"title": "x" * 5000, "body": "y" * 5000, "userId": 1}
    r = requests.post(f"{BASE}/posts", json=payload, timeout=10)
    assert r.status_code < 500, "server error on a 5000-character field"


@pytest.mark.negative
@pytest.mark.security
def test_script_in_title_is_not_executed_or_altered_into_html():
    payload = {"title": "<script>alert(1)</script>", "body": "b", "userId": 1}
    r = requests.post(f"{BASE}/posts", json=payload, timeout=10)
    assert r.headers["Content-Type"].startswith("application/json")
    assert r.json()["title"] == payload["title"]


@pytest.mark.security
def test_responses_do_not_leak_sensitive_fields():
    r, _ = timed_get("/users/1")
    keys = {k.lower() for k in r.json()}
    assert not keys & {"password", "token", "secret", "ssn"}
