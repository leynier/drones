from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, Field

from .data.database import DroneModelType, DroneState


class IdSchema(BaseModel):
    id: UUID


class DroneBaseSchema(BaseModel):
    serial_number: str = Field(max_length=100)
    model: DroneModelType
    weight_limit: int = Field(gt=0, le=500)
    battery_capacity: float = Field(ge=0, le=100)
    state: DroneState


class DroneGetSchema(DroneBaseSchema, IdSchema):
    pass


class DroneGetDetailsSchema(DroneGetSchema):
    medications: list["MedicationGetSchema"]


class DronePostSchema(DroneBaseSchema):
    pass


class MedicationBaseSchema(BaseModel):
    name: str = Field(regex="^[A-Za-z0-9_-]*$")
    weight: int = Field(gt=0)
    code: str = Field(regex="^[A-Z0-9_]*$")
    image: AnyHttpUrl


class MedicationGetSchema(MedicationBaseSchema, IdSchema):
    drone_id: UUID


class MedicationPostSchema(MedicationBaseSchema):
    pass


DroneGetSchema.update_forward_refs()
DroneGetDetailsSchema.update_forward_refs()
DronePostSchema.update_forward_refs()
MedicationGetSchema.update_forward_refs()
MedicationPostSchema.update_forward_refs()
