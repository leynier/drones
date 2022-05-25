from typing import Iterable
from uuid import UUID

import pytest
from drones.deps import get_drone_repository, get_medication_repository
from drones.main import app
from fastapi.testclient import TestClient

from .mocks import get_drone_mock_repository, get_medication_mock_repository

app.dependency_overrides[get_drone_repository] = get_drone_mock_repository
app.dependency_overrides[get_medication_repository] = get_medication_mock_repository


@pytest.fixture(name="client")
def create_client() -> Iterable[TestClient]:
    with TestClient(app) as client:
        yield client


def test_post_drone(client: TestClient) -> None:
    drone = {
        "serial_number": "12345678901234567890123456789012",
        "model": 0,
        "weight_limit": 100,
        "battery_capacity": 100,
        "state": 0,
    }
    response = client.post("/drones/", json=drone)
    response.raise_for_status()
    data = response.json()
    assert data
    assert isinstance(data, dict)
    assert "id" in data
    assert data["id"]
    assert UUID(data["id"])
    del data["id"]
    assert data == drone


@pytest.mark.depends(on=[test_post_drone.__name__])
def test_get_drone(client: TestClient) -> None:
    drone = {
        "serial_number": "12345678901234567890123456789012",
        "model": 0,
        "weight_limit": 100,
        "battery_capacity": 100,
        "state": 0,
    }
    response = client.get("/drones/", json=drone)
    response.raise_for_status()
    data = response.json()
    assert data
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]
    assert isinstance(data[0], dict)
    assert "id" in data[0]
    assert data[0]["id"]
    assert UUID(data[0]["id"])
    data_id = data[0]["id"]
    del data[0]["id"]
    assert data[0] == drone

    response = client.get(f"/drones/{data_id}")
    response.raise_for_status()
    data = response.json()
    assert data
    assert isinstance(data, dict)
    assert "id" in data
    assert data["id"]
    assert UUID(data["id"])
    assert data["id"] == data_id
    del data["id"]
    assert "medications" in data
    assert isinstance(data["medications"], list)
    assert len(data["medications"]) == 0
    del data["medications"]
    assert data == drone
