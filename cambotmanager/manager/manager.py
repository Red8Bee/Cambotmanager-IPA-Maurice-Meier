from cambot_handler import CambotHandler
from models.inventory import Inventory
from storage_handler import StorageHandler


class Manager:
    cambot_handler = CambotHandler()
    storage_handler = StorageHandler()
    inventory = Inventory()

    # This class handles the communication between robot and API and serves data to the API
    # status
    def get_status(self):
        status = "not implemented"
        return status

    def reset_cambot(self):
        status = "not implemented"
        return status
