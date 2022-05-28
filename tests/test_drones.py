from http import HTTPStatus
from typing import Iterable

import pytest
from dirty_equals import (
    HasLen,
    IsAnyStr,
    IsDict,
    IsFloat,
    IsInt,
    IsList,
    IsPartialDict,
    IsUUID,
)
from drones.data.database import new_uuid
from drones.main import app
from drones.settings import Settings, get_settings
from fastapi.testclient import TestClient
from mimesis.providers import Internet, Numeric, Person


@pytest.fixture(name="settings")
def fixture_settings() -> Settings:
    return get_settings()


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
drone_id = str(new_uuid())
medication = {}
medication_id = str(new_uuid())


def test_index_redirect_to_docs(client: TestClient) -> None:
    response = client.get("/", allow_redirects=False)
    assert response.is_redirect


def test_post_drone(
    client: TestClient,
    faker_numeric: Numeric,
    settings: Settings,
) -> None:
    global drone, drone_id
    drone = {
        "serial_number": str(faker_numeric.integer_number(start=0, end=10**6)),
        "model": faker_numeric.integer_number(start=0, end=3),
        "weight_limit": faker_numeric.integer_number(start=1, end=400),
        "battery_capacity": faker_numeric.integer_number(
            start=settings.min_battery_capacity_for_loading + 1, end=100
        ),
        "state": faker_numeric.integer_number(start=0, end=5),
    }
    response = client.post("/drones", json=drone)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == IsPartialDict(**drone)
    assert data == IsPartialDict(id=IsUUID)
    drone_id = data["id"]


@pytest.mark.depends(on=[test_post_drone.__name__])
def test_get_drone(client: TestClient) -> None:
    response = client.get(f"/drones/{drone_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == IsPartialDict(**drone)
    assert data == IsPartialDict(id=drone_id)


@pytest.mark.depends(on=[test_get_drone.__name__])
def test_get_drones(client: TestClient) -> None:
    response = client.get("/drones", json=drone)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == IsList(
        IsPartialDict(
            id=IsUUID,
            serial_number=IsAnyStr(max_length=100),
            model=IsInt(ge=0, le=3),
            weight_limit=IsInt(gt=0, le=500),
            battery_capacity=IsFloat(ge=0, le=100),
            state=IsInt(ge=0, le=5),
        )
    )


@pytest.mark.depends(on=[test_get_drones.__name__])
def test_get_drones_by_state(client: TestClient) -> None:
    response = client.get("/drones", params={"state": drone["state"]})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == IsList(
        IsPartialDict(
            id=IsUUID,
            serial_number=IsAnyStr(max_length=100),
            model=IsInt(ge=0, le=3),
            weight_limit=IsInt(gt=0, le=500),
            battery_capacity=IsFloat(ge=0, le=100),
            state=IsInt(ge=0, le=5),
        ),
        check_order=False,
    )


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
        "weight": faker_numeric.integer_number(start=1, end=drone["weight_limit"] - 1),
        "code": str(faker_numeric.integer_number(start=0)),
        "image": faker_internet.url(),
    }
    response = client.post(f"/drones/{drone_id}/medications", json=medication)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == IsPartialDict(**medication)
    assert data == IsPartialDict(id=IsUUID, drone_id=drone_id)
    medication_id = data["id"]


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
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == IsList(IsPartialDict(**medication, id=str(medication_id)))


@pytest.mark.depends(on=[test_get_medication.__name__])
def test_delete_medication(client: TestClient) -> None:
    response = client.delete(f"/drones/{drone_id}/medications/{medication_id}")
    assert response.status_code == 200, response.text


@pytest.mark.depends(on=[test_delete_medication.__name__])
def test_get_medication_not_found(client: TestClient) -> None:
    response = client.get(f"/drones/{drone_id}/medications")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == IsList()
    assert data == HasLen(0)


@pytest.mark.depends(on=[test_get_medication_not_found.__name__])
def test_delete_drone(client: TestClient) -> None:
    response = client.delete(f"/drones/{drone_id}")
    assert response.status_code == 200, response.text


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
        "weight": faker_numeric.integer_number(start=1, end=drone["weight_limit"] - 1),
        "code": str(faker_numeric.integer_number(start=0)),
        "image": faker_internet.url(),
    }
    response = client.post(f"/drones/{drone_id}/medications", json=medication)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.depends(on=[test_delete_medication.__name__])
def test_delete_medication_not_found_in_delete(client: TestClient) -> None:
    response = client.delete(f"/drones/{drone_id}/medications/{medication_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_insert_drone_with_low_of_batery(
    client: TestClient,
    faker_internet: Internet,
    faker_numeric: Numeric,
    faker_person: Person,
    settings: Settings,
) -> None:
    drone = {
        "serial_number": str(faker_numeric.integer_number(start=0, end=10**6)),
        "model": faker_numeric.integer_number(start=0, end=3),
        "weight_limit": faker_numeric.integer_number(start=1, end=400),
        "battery_capacity": faker_numeric.integer_number(
            start=0,
            end=settings.min_battery_capacity_for_loading - 1,
        ),
        "state": faker_numeric.integer_number(start=0, end=5),
    }
    response = client.post("/drones", json=drone)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == IsPartialDict(**drone, id=IsUUID)
    drone_id = data["id"]
    medication = {
        "name": faker_person.name(),
        "weight": faker_numeric.integer_number(start=1, end=drone["weight_limit"] - 1),
        "code": str(faker_numeric.integer_number(start=0)),
        "image": faker_internet.url(),
    }
    response = client.post(f"/drones/{drone_id}/medications", json=medication)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    response = client.delete(f"/drones/{drone_id}")
    assert response.status_code == 200, response.text
