from fastapi import HTTPException, Request

from .services.drone_service import (
    DroneCantBeDeletedError,
    DroneCantLoadMedicationsError,
    DroneNotFoundError,
    MedicationNotFoundError,
)


def drone_cant_be_deleted_handler(
    _: Request,
    exc: DroneCantBeDeletedError,
) -> None:
    raise HTTPException(
        status_code=400,
        detail=f"Drone cannot be deleted: {exc.args[0]}",
    )


def drone_not_found_handler(
    _: Request,
    exc: DroneNotFoundError,
) -> None:
    raise HTTPException(
        status_code=404,
        detail=f"Drone not found: {exc.args[0]}",
    )


def drone_cant_load_medications_handler(
    _: Request,
    exc: DroneCantLoadMedicationsError,
) -> None:
    raise HTTPException(
        status_code=400,
        detail=f"Drone cannot load medications: {exc.args[0]}",
    )


def medication_not_found_handler(
    _: Request,
    exc: MedicationNotFoundError,
) -> None:
    raise HTTPException(
        status_code=404,
        detail=f"Medication not found: {exc.args[0]}",
    )
