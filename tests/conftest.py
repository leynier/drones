from drones.deps import get_drone_repository, get_medication_repository
from drones.main import app
from pytest import Config, Parser

from .mocks import get_drone_mock_repository, get_medication_mock_repository


def pytest_addoption(parser: Parser):
    parser.addoption("--mode", action="store", default="mock")


def pytest_configure(config: Config):
    if config.option.mode == "mock":  # type: ignore
        app.dependency_overrides[get_drone_repository] = get_drone_mock_repository
        app.dependency_overrides[
            get_medication_repository
        ] = get_medication_mock_repository
