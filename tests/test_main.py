from fastapi.testclient import TestClient
import pytest

def test_notify_backend(test_client: TestClient):
    response = test_client.post("/notify_backend", json={"city_name": "Berlin"})
    assert response.status_code == 200
    data = response.json()
    assert data["city_name"] == "Berlin"
    assert "sessid" in data

def test_analytics(test_client: TestClient):
    test_client.post("/notify_backend", json={"city_name": "Munich"})
    test_client.post("/notify_backend", json={"city_name": "Munich"})
    
    response = test_client.get("/analytics")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["total"], int)
    assert isinstance(data["items"], list)

    response = test_client.get("/analytics", params={"city_name": "Munich"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert all(item["city_name"] == "Munich" for item in data["items"])

    response = test_client.get("/analytics", params={"sessid": "no-such"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []
