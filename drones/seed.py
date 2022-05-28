from typing import cast

from pydantic import AnyHttpUrl

from .deps import DroneServiceWithoutDepends
from .schemas import DroneModelType, DronePostSchema, DroneState, MedicationPostSchema
from .settings import Settings


def run_seed(settings: Settings):
    """
    This function is used to seed the database with data.
    """
    with DroneServiceWithoutDepends() as service:
        drones_post = [
            DronePostSchema(
                serial_number="123456789",
                battery_capacity=100,
                weight_limit=100,
                model=DroneModelType.Middleweight,
                state=DroneState.IDLE,
            ),
            DronePostSchema(
                serial_number="987654321",
                battery_capacity=50,
                weight_limit=400,
                model=DroneModelType.Lightweight,
                state=DroneState.IDLE,
            ),
        ]
        drones = [service.add_drone(drone) for drone in drones_post]
        medications_post = [
            MedicationPostSchema(
                name="Aspirin",
                code="A",
                image=cast(
                    AnyHttpUrl, "https://www.aspirin.com/images/aspirin-logo.png"
                ),
                weight=10,
            ),
            MedicationPostSchema(
                name="Advil",
                code="B",
                image=cast(AnyHttpUrl, "https://www.advil.com/images/advil-logo.png"),
                weight=20,
            ),
        ]
        for index, medication in enumerate(medications_post):
            service.add_medication(drone_id=drones[index].id, medication=medication)
    with open(settings.Config.env_file, mode="a") as file:
        file.write("\nSEED=false\n")
