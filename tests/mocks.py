from uuid import UUID

from drones.data.database import Drone, DroneState, Medication

mocked_drones: list[Drone] = []
mocked_medications: list[Medication] = []


class DroneMockRepository:
    def add_drone(self, drone: Drone) -> Drone:
        mocked_drones.append(drone)
        return drone

    def remove_drone(self, drone: Drone) -> None:
        global mocked_drones
        mocked_drones = [d for d in mocked_drones if d.id != drone.id]

    def get_drones(self, state: DroneState | None = None) -> list[Drone]:
        return [d for d in mocked_drones if state is None or d.state == state]

    def get_drone(self, drone_id: UUID) -> Drone | None:
        return next((d for d in mocked_drones if d.id == drone_id), None)


def get_drone_mock_repository() -> DroneMockRepository:
    return DroneMockRepository()


class MedicationMockRepository:
    def add_medication(self, medication: Medication) -> Medication:
        mocked_medications.append(medication)
        return medication

    def remove_medication(self, medication: Medication) -> None:
        global mocked_medications
        mocked_medications = [m for m in mocked_medications if m.id != medication.id]

    def get_medications(self, drone_id: UUID | None = None) -> list[Medication]:
        return [
            m for m in mocked_medications if drone_id is None or m.drone_id == drone_id
        ]

    def get_medication(self, medication_id: UUID) -> Medication | None:
        return next((m for m in mocked_medications if m.id == medication_id), None)


def get_medication_mock_repository() -> MedicationMockRepository:
    return MedicationMockRepository()
