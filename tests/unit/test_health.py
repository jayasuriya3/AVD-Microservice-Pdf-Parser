from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_correlation_id_is_propagated() -> None:
    response = TestClient(app).get("/health", headers={"x-correlation-id": "test-correlation"})
    assert response.headers["x-correlation-id"] == "test-correlation"
