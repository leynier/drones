from functools import cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///drones.db"
    database_debug: bool = False


__settings: Settings | None = None


def get_settings():
    global __settings
    if __settings is None:
        __settings = Settings()
    return __settings
