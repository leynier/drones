from uuid import UUID

from sqlmodel import Session, select

from ..data.database import Drone, DroneState


class DroneRepository:
    def __init__(self, session: Session) -> None:
        self.__session = session

    def add_drone(self, drone: Drone) -> Drone:
        self.__session.add(drone)
        self.__session.commit()
        self.__session.refresh(drone)
        return drone

    def remove_drone(self, drone: Drone) -> None:
        self.__session.delete(drone)
        self.__session.commit()

    def get_drones(self, state: DroneState | None = None) -> list[Drone]:
        query = select(Drone)
        if state is not None:
            query = query.where(Drone.state == state)
        drones = self.__session.exec(query).all()
        return drones

    def get_drone(self, drone_id: UUID) -> Drone | None:
        query = select(Drone).where(Drone.id == drone_id)
        drone = self.__session.exec(query).first()
        return drone
