from fastapi import FastAPI
from fastapi_control import add_controllers

# For import all controllers dynamically
from . import controllers  # noqa: F401, F403
from .controllers import *  # noqa: F401, F403

app = FastAPI()
add_controllers(app)
