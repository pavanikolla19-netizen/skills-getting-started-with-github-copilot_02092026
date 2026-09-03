from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_delete_participant_removes_email_from_activity():
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

    # restore state for subsequent tests
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )


def test_delete_participant_returns_404_for_unknown_activity():
    response = client.delete(
        "/activities/Nonexistent Club/participants",
        params={"email": "someone@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
