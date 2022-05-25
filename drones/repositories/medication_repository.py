from uuid import UUID

from sqlmodel import Session, select

from ..data.database import Medication


class MedicationRepository:
    def __init__(self, session: Session) -> None:
        self.__session = session

    def add_medication(self, medication: Medication) -> Medication:
        self.__session.add(medication)
        self.__session.commit()
        self.__session.refresh(medication)
        return medication

    def remove_medication(self, medication: Medication) -> None:
        self.__session.delete(medication)
        self.__session.commit()

    def get_medications(self, drone_id: UUID | None = None) -> list[Medication]:
        query = select(Medication)
        if drone_id is not None:
            query = query.where(Medication.drone_id == drone_id)
        medications = self.__session.exec(query).all()
        return medications

    def get_medication(self, medication_id: UUID) -> Medication | None:
        query = select(Medication).where(Medication.id == medication_id)
        medication = self.__session.exec(query).first()
        return medication
