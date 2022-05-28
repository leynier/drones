from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_url: str = "sqlite:///drones.db"
    database_debug: bool = False

    min_battery_capacity_for_loading: int = 25

    time_interval_battery: int = 5
    logger_drones_batteries_capacity_file_path: str = "drones_batteries_capacity.log"
    logger_drones_batteries_capacity_name: str = "drones_batteries_capacity"

    seed: bool = True

    class Config:
        env_file = ".env"


__settings: Settings | None = None


def get_settings():
    global __settings
    if __settings is None:
        __settings = Settings()
    return __settings
