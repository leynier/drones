from functools import cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///drones.db"
    database_debug: bool = False


@cache
def get_settings():
    return Settings()
