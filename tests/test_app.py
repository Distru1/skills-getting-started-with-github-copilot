from fastapi.testclient import TestClient
from urllib.parse import quote

from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()

    assert "Programming Class" in data


def test_signup_and_unregister_flow():
    activity = "Soccer Team"
    email = "alice@example.com"

    # Ensure participant not present initially
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert email not in data[activity]["participants"]

    # Sign up
    signup_resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert signup_resp.status_code == 200
    assert "Signed up" in signup_resp.json().get("message", "")

    # Check participant was added
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert email in data2[activity]["participants"]

    # Signing up same email again should return 400
    dup_resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert dup_resp.status_code == 400

    # Unregister
    del_resp = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    assert del_resp.status_code == 200
    assert "Removed" in del_resp.json().get("message", "")

    # Ensure participant removed
    resp3 = client.get("/activities")
    data3 = resp3.json()
    assert email not in data3[activity]["participants"]
