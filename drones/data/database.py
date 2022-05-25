from enum import IntEnum, auto
from typing import Iterable
from uuid import UUID, uuid4

import sqlalchemy as sqla
from fastapi import Depends
from pydantic import AnyHttpUrl
from sqlmodel import Field, Session, SQLModel, create_engine
from sqlmodel.sql.expression import Select, SelectOfScalar

from ..settings import Settings, get_settings

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


__engine: sqla.engine.Engine | None = None


def get_engine(settings: Settings = Depends(get_settings)) -> sqla.engine.Engine:
    global __engine
    if __engine is None:
        __engine = create_engine(settings.database_url, echo=settings.database_debug)
    return __engine


def get_session(engine: sqla.engine.Engine = Depends(get_engine)) -> Iterable[Session]:
    with Session(engine) as session:
        yield session


class DroneModelType(IntEnum):
    Lightweight = auto()
    Middleweight = auto()
    Cruiserweight = auto()
    Heavyweight = auto()


class DroneState(IntEnum):
    IDLE = auto()
    LOADING = auto()
    LOADED = auto()
    DELIVERING = auto()
    DELIVERED = auto()
    RETURNING = auto()


class Drone(SQLModel, table=True):
    __tablename__: str = "drones"
    id: UUID = Field(
        primary_key=True,
        index=True,
        nullable=False,
        default_factory=uuid4,
        sa_column_kwargs={
            "server_default": sqla.text("uuid_generate_v4()"),
        },
    )
    serial_number: str = Field(max_length=100, index=True, nullable=False)
    model: DroneModelType = Field(nullable=False)
    weight_limit: int = Field(gt=0, le=500, nullable=False)
    battery_capacity: float = Field(ge=0, le=100, nullable=False)
    state: DroneState = Field(nullable=False)


class Medication(SQLModel, table=True):
    __tablename__: str = "medications"
    id: UUID = Field(
        primary_key=True,
        index=True,
        nullable=False,
        default_factory=uuid4,
        sa_column_kwargs={
            "server_default": sqla.text("uuid_generate_v4()"),
        },
    )
    name: str = Field(regex="^[A-Za-z0-9_-]*$", nullable=False)
    weight: int = Field(ge=0, nullable=False)
    code: str = Field(regex="^[A-Z0-9_]*$", index=True, nullable=False)
    image: AnyHttpUrl = Field(nullable=False)
    drone_id: UUID = Field(foreign_key="drones.id", index=True, nullable=False)
