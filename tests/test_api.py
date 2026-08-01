from fastapi.testclient import TestClient

from enerjinabiz.api import app


def test_health_and_hourly_endpoints():
    client = TestClient(app)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    hourly = client.get("/hourly?limit=3")
    assert hourly.status_code == 200
    assert len(hourly.json()) == 3
