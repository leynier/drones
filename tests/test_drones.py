from http import HTTPStatus
from typing import Iterable
from uuid import UUID, uuid4

import pytest
from dirty_equals import HasLen, IsList, IsPartialDict, IsUUID
from drones.deps import get_drone_repository, get_medication_repository
from drones.main import app
from fastapi.testclient import TestClient
from mimesis.providers import Internet, Numeric, Person

from .conftest import option
from .mocks import get_drone_mock_repository, get_medication_mock_repository

if option.mode == "mock":  # type: ignore
    app.dependency_overrides[get_drone_repository] = get_drone_mock_repository
    app.dependency_overrides[get_medication_repository] = get_medication_mock_repository


@pytest.fixture(name="faker_internet")
def fixture_faker_internet() -> Internet:
    return Internet()


@pytest.fixture(name="faker_numeric")
def faker_hadware_fixture() -> Numeric:
    return Numeric()


@pytest.fixture(name="faker_person")
def faker_person_fixture() -> Person:
    return Person()


@pytest.fixture(name="client")
def client_fixture() -> Iterable[TestClient]:
    with TestClient(app) as client:
        yield client


drone = {}
drone_id = uuid4()
medication = {}
medication_id = uuid4()


def test_index_redirect_to_docs(client: TestClient) -> None:
    response = client.get("/", allow_redirects=False)
    assert response.is_redirect


def test_post_drone(
    client: TestClient,
    faker_numeric: Numeric,
) -> None:
    global drone, drone_id
    drone = {
        "serial_number": str(faker_numeric.integer_number(start=0, end=10**6)),
        "model": faker_numeric.integer_number(start=0, end=3),
        "weight_limit": faker_numeric.integer_number(start=1, end=400),
        "battery_capacity": faker_numeric.integer_number(start=0, end=100),
        "state": faker_numeric.integer_number(start=0, end=5),
    }
    response = client.post("/drones", json=drone)
    response.raise_for_status()
    data = response.json()
    assert data == IsPartialDict(**drone)
    assert data == IsPartialDict(id=IsUUID)
    drone_id = UUID(data["id"])


@pytest.mark.depends(on=[test_post_drone.__name__])
def test_get_drone(client: TestClient) -> None:
    response = client.get(f"/drones/{drone_id}")
    response.raise_for_status()
    data = response.json()
    assert data == IsPartialDict(**drone)
    assert data == IsPartialDict(id=str(drone_id))


@pytest.mark.depends(on=[test_get_drone.__name__])
def test_get_drones(client: TestClient) -> None:
    response = client.get("/drones", json=drone)
    response.raise_for_status()
    data = response.json()
    assert data == IsList(IsPartialDict(**drone, id=str(drone_id)))


@pytest.mark.depends(on=[test_get_drones.__name__])
def test_get_drones_by_state(client: TestClient) -> None:
    response = client.get("/drones", params={"state": drone["state"]})
    response.raise_for_status()
    data = response.json()
    assert data == IsList(IsPartialDict(**drone, id=str(drone_id)))


@pytest.mark.depends(on=[test_get_drones_by_state.__name__])
def test_post_medication(
    client: TestClient,
    faker_internet: Internet,
    faker_numeric: Numeric,
    faker_person: Person,
) -> None:
    global medication, medication_id
    medication = {
        "name": faker_person.name(),
        "weight": faker_numeric.integer_number(start=1, end=drone["weight_limit"]),
        "code": str(faker_numeric.integer_number(start=0)),
        "image": faker_internet.url(),
    }
    response = client.post(f"/drones/{drone_id}/medications", json=medication)
    response.raise_for_status()
    data = response.json()
    assert data == IsPartialDict(**medication)
    assert data == IsPartialDict(id=IsUUID, drone_id=str(drone_id))
    medication_id = UUID(data["id"])


@pytest.mark.depends(on=[test_post_medication.__name__])
def test_post_medications_over_weight(
    client: TestClient,
    faker_internet: Internet,
    faker_numeric: Numeric,
    faker_person: Person,
) -> None:
    medication = {
        "name": faker_person.name(),
        "weight": faker_numeric.integer_number(
            start=drone["weight_limit"] + 1,
            end=drone["weight_limit"] + 5,
        ),
        "code": str(faker_numeric.integer_number(start=0)),
        "image": faker_internet.url(),
    }
    response = client.post(f"/drones/{drone_id}/medications", json=medication)
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.depends(on=[test_post_medications_over_weight.__name__])
def test_delete_drone_with_medications(client: TestClient) -> None:
    response = client.delete(f"/drones/{drone_id}")
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.depends(on=[test_delete_drone_with_medications.__name__])
def test_get_medication(client: TestClient) -> None:
    response = client.get(f"/drones/{drone_id}/medications")
    response.raise_for_status()
    data = response.json()
    assert data == IsList(IsPartialDict(**medication, id=str(medication_id)))


@pytest.mark.depends(on=[test_get_medication.__name__])
def test_delete_medication(client: TestClient) -> None:
    response = client.delete(f"/drones/{drone_id}/medications/{medication_id}")
    response.raise_for_status()


@pytest.mark.depends(on=[test_delete_medication.__name__])
def test_get_medication_not_found(client: TestClient) -> None:
    response = client.get(f"/drones/{drone_id}/medications")
    response.raise_for_status()
    data = response.json()
    assert data == IsList()
    assert data == HasLen(0)


@pytest.mark.depends(on=[test_get_medication_not_found.__name__])
def test_delete_drone(client: TestClient) -> None:
    response = client.delete(f"/drones/{drone_id}")
    response.raise_for_status()


@pytest.mark.depends(on=[test_delete_drone.__name__])
def test_get_drone_not_found_in_get(client: TestClient) -> None:
    response = client.get(f"/drones/{drone_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.depends(on=[test_delete_drone.__name__])
def test_delete_drone_not_found_in_delete(client: TestClient) -> None:
    response = client.delete(f"/drones/{drone_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.depends(on=[test_delete_drone.__name__])
def test_post_medication_not_found_in_post(
    client: TestClient,
    faker_internet: Internet,
    faker_numeric: Numeric,
    faker_person: Person,
) -> None:
    medication = {
        "name": faker_person.name(),
        "weight": faker_numeric.integer_number(start=1, end=drone["weight_limit"]),
        "code": str(faker_numeric.integer_number(start=0)),
        "image": faker_internet.url(),
    }
    response = client.post(f"/drones/{drone_id}/medications", json=medication)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.depends(on=[test_delete_medication.__name__])
def test_delete_medication_not_found_in_delete(client: TestClient) -> None:
    response = client.delete(f"/drones/{drone_id}/medications/{medication_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_insert_drone_with_20_of_batery(
    client: TestClient,
    faker_internet: Internet,
    faker_numeric: Numeric,
    faker_person: Person,
) -> None:
    drone = {
        "serial_number": str(faker_numeric.integer_number(start=0, end=10**6)),
        "model": faker_numeric.integer_number(start=0, end=3),
        "weight_limit": faker_numeric.integer_number(start=1, end=400),
        "battery_capacity": faker_numeric.integer_number(start=0, end=20),
        "state": faker_numeric.integer_number(start=0, end=5),
    }
    response = client.post("/drones", json=drone)
    response.raise_for_status()
    data = response.json()
    assert data == IsPartialDict(**drone, id=IsUUID)
    drone_id = UUID(data["id"])
    medication = {
        "name": faker_person.name(),
        "weight": faker_numeric.integer_number(start=1, end=drone["weight_limit"]),
        "code": str(faker_numeric.integer_number(start=0)),
        "image": faker_internet.url(),
    }
    response = client.post(f"/drones/{drone_id}/medications", json=medication)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    response = client.delete(f"/drones/{drone_id}")
    response.raise_for_status()
