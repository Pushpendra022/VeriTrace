from fastapi.testclient import TestClient

from app.main import app


def test_health_reports_database_and_provider() -> None:
    with TestClient(app) as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": "connected",
        "llm_provider": "gemini",
    }

