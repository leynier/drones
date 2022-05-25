from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .handlers import (
    drone_cant_be_deleted_handler,
    drone_cant_load_medications_handler,
    drone_not_found_handler,
    medication_not_found_handler,
)
from .routes.drones_router import router as drones_router
from .services.drone_service import (
    DroneCantBeDeletedError,
    DroneCantLoadMedicationsError,
    DroneNotFoundError,
    MedicationNotFoundError,
)

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
