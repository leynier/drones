from fastapi import Depends
from sqlmodel import Session

from .data.database import get_session
from .repositories.drone_repository import DroneRepository
from .repositories.medication_repository import MedicationRepository
from .services.drone_service import DroneService
from .settings import Settings, get_settings


def get_drone_repository(session: Session = Depends(get_session)) -> DroneRepository:
    return DroneRepository(session)


def get_medication_repository(
    session: Session = Depends(get_session),
) -> MedicationRepository:
    return MedicationRepository(session)


def get_drone_service(
    drone_repository: DroneRepository = Depends(get_drone_repository),
    medication_repository: MedicationRepository = Depends(get_medication_repository),
    settings: Settings = Depends(get_settings),
) -> DroneService:
    return DroneService(
        drone_repository,
        medication_repository,
        settings.min_battery_capacity_for_loading,
    )
