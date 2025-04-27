from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_initiate_file_upload_success():
    response = client.post(
        "/api/upload",
        headers={"access_token": "supersecretapikey123"},
        json={"user_id": "abc123", "file_name": "document.pdf"}
    )
    assert response.status_code == 202
    assert response.json()["status"] == "pending"

def test_initiate_file_upload_auth_failure():
    response = client.post(
        "/api/upload",
        headers={"access_token": "wrongapikey"},
        json={"user_id": "abc123", "file_name": "document.pdf"}
    )
    assert response.status_code == 403

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}