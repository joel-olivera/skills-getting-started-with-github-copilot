import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code in (200, 307, 200)  # 307 for redirect, 200 for static

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data
    assert "participants" in data["Soccer Team"]

def test_signup_success():
    response = client.post("/activities/Math Club/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Clean up: remove the test participant
    data = client.get("/activities").json()
    data["Math Club"]["participants"].remove("tester@mergington.edu")

def test_signup_duplicate():
    # Add a participant
    client.post("/activities/Drama Club/signup?email=dupe@mergington.edu")
    # Try to add again
    response = client.post("/activities/Drama Club/signup?email=dupe@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    data = client.get("/activities").json()
    data["Drama Club"]["participants"].remove("dupe@mergington.edu")

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
