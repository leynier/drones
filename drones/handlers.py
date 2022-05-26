from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

from .services.drone_service import (
    DroneCantBeDeletedError,
    DroneCantLoadMedicationsError,
    DroneNotFoundError,
    MedicationNotFoundError,
)


def drone_cant_be_deleted_handler(
    _: Request,
    exc: DroneCantBeDeletedError,
) -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"details": f"Drone cannot be deleted: {exc.args[0]}"},
    )


def drone_not_found_handler(
    _: Request,
    exc: DroneNotFoundError,
) -> Response:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"details": f"Drone not found: {exc.args[0]}"},
    )


def drone_cant_load_medications_handler(
    _: Request,
    exc: DroneCantLoadMedicationsError,
) -> Response:
    return JSONResponse(
        status_code=400,
        content={"details": f"Drone cannot load medications: {exc.args[0]}"},
    )


def medication_not_found_handler(
    _: Request,
    exc: MedicationNotFoundError,
) -> Response:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"details": f"Medication not found: {exc.args[0]}"},
    )
