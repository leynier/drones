from uuid import UUID

from pydantic import parse_obj_as

from ..data.database import Drone, DroneState, Medication
from ..repositories.drone_repository import DroneRepository
from ..repositories.medication_repository import MedicationRepository
from ..schemas import (
    DroneGetDetailsSchema,
    DroneGetSchema,
    DronePostSchema,
    MedicationGetSchema,
    MedicationPostSchema,
)


class DroneNotFoundError(Exception):
    pass


class DroneCantBeDeletedError(Exception):
    pass


class DroneCantLoadMedicationsError(Exception):
    pass


class MedicationNotFoundError(Exception):
    pass


class DroneService:
    def __init__(
        self,
        drone_repository: DroneRepository,
        medication_repository: MedicationRepository,
    ) -> None:
        self.__drone_repository = drone_repository
        self.__medication_repository = medication_repository

    def add_drone(self, drone: DronePostSchema) -> DroneGetSchema:
        entity = Drone(**drone.dict())
        self.__drone_repository.add_drone(entity)
        return DroneGetSchema(**entity.dict())

    def remove_drone(self, drone_id: UUID) -> None:
        entity = self.__drone_repository.get_drone(drone_id)
        if entity is None:
            raise DroneNotFoundError("Drone not found")
        medications = self.__medication_repository.get_medications(drone_id)
        if not medications:
            raise DroneCantBeDeletedError("Drone cannot be deleted")
        self.__drone_repository.remove_drone(entity)

    def get_drones(self, state: DroneState | None = None) -> list[DroneGetSchema]:
        entities = self.__drone_repository.get_drones(state)
        return parse_obj_as(list[DroneGetSchema], entities)

    def get_drone(self, drone_id: UUID) -> DroneGetDetailsSchema:
        entity = self.__drone_repository.get_drone(drone_id)
        if entity is None:
            raise DroneNotFoundError("Drone not found")
        medications = self.__medication_repository.get_medications(drone_id)
        return DroneGetDetailsSchema(
            **entity.dict(),
            medications=parse_obj_as(list[MedicationGetSchema], medications),
        )

    def add_medication(
        self,
        drone_id: UUID,
        medication: MedicationPostSchema,
    ) -> MedicationGetSchema:
        entity = self.__drone_repository.get_drone(drone_id)
        if entity is None:
            raise DroneNotFoundError("Drone not found")
        medications = self.__medication_repository.get_medications(drone_id)
        total_weight = sum(medication.weight for medication in medications)
        if total_weight + medication.weight > entity.weight_limit:
            raise DroneCantLoadMedicationsError("Drone cannot load medication")
        entity = Medication(**medication.dict())
        self.__medication_repository.add_medication(entity)
        return MedicationGetSchema(**entity.dict())

    def remove_medication(self, drone_id: UUID, medication_id: UUID) -> None:
        entity = self.__medication_repository.get_medication(medication_id)
        if entity is None or entity.drone_id != drone_id:
            raise MedicationNotFoundError("Medication not found")
        self.__medication_repository.remove_medication(entity)
