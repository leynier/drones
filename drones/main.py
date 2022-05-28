import logging

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi_restful.tasks import repeat_every

from .deps import DroneServiceWithoutDepends
from .handlers import (
    drone_cant_be_deleted_handler,
    drone_cant_load_medications_handler,
    drone_not_found_handler,
    medication_not_found_handler,
)
from .loggers import config_loggers
from .routes.drones_router import router as drones_router
from .services.drone_service import (
    DroneCantBeDeletedError,
    DroneCantLoadMedicationsError,
    DroneNotFoundError,
    MedicationNotFoundError,
)
from .settings import get_settings

config_loggers()

app = FastAPI(
    title="Drones API",
    description="A solution for the technical task of the recruitment process of Musala Soft.",
)
app.include_router(drones_router, prefix="/drones")
app.add_exception_handler(
    DroneCantBeDeletedError,
    drone_cant_be_deleted_handler,
)
app.add_exception_handler(
    DroneCantLoadMedicationsError,
    drone_cant_load_medications_handler,
)
app.add_exception_handler(
    DroneNotFoundError,
    drone_not_found_handler,
)
app.add_exception_handler(
    MedicationNotFoundError,
    medication_not_found_handler,
)


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs")


@app.on_event("startup")
@repeat_every(seconds=get_settings().time_interval_battery)
def startup():
    logger_name = get_settings().logger_drones_batteries_capacity_name
    logger = logging.getLogger(logger_name)
    with DroneServiceWithoutDepends() as service:
        drones = service.get_drones()
        for drone in drones:
            logger.info(
                f"Drone id: {drone.id}, "
                + f"serial number: {drone.serial_number}, "
                + f"battery capacity: {drone.battery_capacity}%"
            )
