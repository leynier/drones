from uuid import UUID

from fastapi import APIRouter, Depends

from ..data.database import DroneState
from ..deps import get_drone_service
from ..schemas import (
    DroneGetDetailsSchema,
    DroneGetSchema,
    DronePostSchema,
    MedicationGetSchema,
    MedicationPostSchema,
)
from ..services.drone_service import DroneService

router = APIRouter(tags=["Drones"])


@router.get("/", response_model=list[DroneGetSchema])
def get_drones(
    state: DroneState | None = None,
    drone_service: DroneService = Depends(get_drone_service),
):
    return drone_service.get_drones(state)


@router.get("/{drone_id}", response_model=DroneGetDetailsSchema)
def get_drone(
    drone_id: UUID,
    drone_service: DroneService = Depends(get_drone_service),
):
    return drone_service.get_drone(drone_id)


@router.post("/", response_model=DroneGetSchema)
def post_drone(
    drone: DronePostSchema,
    drone_service: DroneService = Depends(get_drone_service),
):
    return drone_service.add_drone(drone)


@router.get("/{drone_id}/medications", response_model=list[MedicationGetSchema])
def get_medications(
    drone_id: UUID,
    drone_service: DroneService = Depends(get_drone_service),
):
    return drone_service.get_drone(drone_id).medications


@router.post("/{drone_id}/medications", response_model=MedicationGetSchema)
def post_medication(
    drone_id: UUID,
    medication: MedicationPostSchema,
    drone_service: DroneService = Depends(get_drone_service),
):
    return drone_service.add_medication(drone_id, medication)


@router.delete("/{drone_id}/medications/{medication_id}")
def delete_medication(
    drone_id: UUID,
    medication_id: UUID,
    drone_service: DroneService = Depends(get_drone_service),
):
    return drone_service.remove_medication(drone_id, medication_id)
