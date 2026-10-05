from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    response.raise_for_status()
    body = response.json()

    assert body["status"] == "healthy"
