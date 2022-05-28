from fastapi import Depends
from sqlmodel import Session

from .data.database import get_engine, get_session
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


class DroneServiceWithoutDepends(DroneService):
    def __init__(self) -> None:
        settings = get_settings()
        engine = get_engine(settings)
        self.__session = Session(engine)
        drone_repository = DroneRepository(self.__session)
        medication_repository = MedicationRepository(self.__session)
        DroneService.__init__(
            self,
            drone_repository,
            medication_repository,
            settings.min_battery_capacity_for_loading,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__session.close()
