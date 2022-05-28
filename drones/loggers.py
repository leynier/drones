import logging

from .settings import get_settings


def config_loggers():
    formater = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formater)
    file_handler_filename = get_settings().logger_drones_batteries_capacity_file_path
    file_handler = logging.FileHandler(file_handler_filename)
    file_handler.setFormatter(formater)
    logger_name = get_settings().logger_drones_batteries_capacity_name
    logger = logging.getLogger(logger_name)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
