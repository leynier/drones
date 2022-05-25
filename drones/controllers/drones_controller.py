from fastapi_control import APIController, controller, get


@controller(prefix="/drones")
class DronesController(APIController):
    @get("")
    def get_drones(self):
        return []
