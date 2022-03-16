import os.path
import shutil

from handlers.cambot_handler import CambotHandler
from handlers.storage_handler import StorageHandler
from models.inventory import Inventory
from models.inventory_item import InventoryItem
from models.config import Config
from models.position import Position
from models.status import Status


def create_folder(base_directory_path):
    if not (os.path.exists(base_directory_path)):
        os.mkdir(base_directory_path)


def remove_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)


def check_if_id_is_UUID(id_to_check):
    return True


class Manager:
    cambot_handler = CambotHandler()
    storage_handler = StorageHandler()
    inventory = Inventory()

    # This class handles the communication between robot/storage and API, serves data to the API
    def __init__(self):
        self.cambot_handler = CambotHandler(self)
        self.storage_handler = StorageHandler(self)
        self.inventory = Inventory()
        self.configs = []
        self.status_enum = ['success', 'fail', 'in_progress', 'in_queue']
        self.storage_status_enum = ['all', 'scheduled_delete', 'stored', 'floating']
        self.robot_status = Status('idle', 200, 'ok', self.storage_handler.max_size - self.storage_handler.size,
                                   Position('home', 0, 0, 0))

    def check_storage(self):
        self.storage_handler.clean_inventory()

    # This class handles the communication between robot and API and serves data to the API
    # status
    def get_status(self):
        status = self.robot_status
        self.check_storage()
        return status

    def reset_cambot(self):
        status = "not implemented"
        self.check_storage()
        return status

    # Inventory
    def create_inventory_item(self, config: Config, id_tag):
        base_directory = '../Inventory/' + id_tag
        item = InventoryItem(config, id_tag, base_directory)
        create_folder(base_directory)
        self.inventory.todo.append(item)
        self.inventory.all_items.append(item)
        self.check_storage()

    def get_whole_inventory(self, status, storage_status):
        params_are_ok = self.check_params(status, storage_status)
        if params_are_ok:
            whole_inventory = self.inventory.all_items
            searched_inventory = []
            for item in whole_inventory:
                if status is not None and item.status == status:
                    searched_inventory.append(item.id_tag)
                elif storage_status is not None and item.storage_status == storage_status:
                    searched_inventory.append(item.id_tag)
                else:
                    searched_inventory.append(item.id_tag)
            self.check_storage()
            return searched_inventory
        self.check_storage()
        return None

    def get_inventory_item(self, id_tag):
        if check_if_id_is_UUID(id_tag):
            whole_inventory = self.inventory.all_items
            for item in whole_inventory:
                if item.id_tag == id_tag:
                    self.check_storage()
                    return item
            self.check_storage()
            return None
        self.check_storage()
        return 'id_invalid'

    def delete_inventory_item(self, id_tag):
        if check_if_id_is_UUID(id_tag):
            for item in self.inventory.all_items:
                if item.id_tag == id_tag:
                    self.inventory.all_items.remove(item)
                    remove_folder(item.base_directory)
                    self.check_storage()
                    return item
            self.check_storage()
            return None
        self.check_storage()
        return 'id_invalid'

    def get_snapshot_from_item(self, id_tag, snapshot_time):
        item = self.get_inventory_item(id_tag)
        if item != "id_invalid":
            for s in item.snapshots:
                if s.time == snapshot_time:
                    self.check_storage()
                    return s
            self.check_storage()
            return None
        self.check_storage()
        return item

    # Config
    def create_config(self, json):
        try:
            config: Config = Config(json['name'], json['description'], json['type'], json['positions'],
                                    json['defaultMaxProgress'])
            self.configs.append(config)
            self.check_storage()
            return True
        except ValueError:
            return False

    def get_config(self, config_id):
        for c in self.configs:
            if c.name == config_id:
                self.check_storage()
                return c
        self.check_storage()
        return None

    def get_all_configs(self):
        all_configs = []
        for c in self.configs:
            all_configs.append(c.name)
        self.check_storage()
        return all_configs

    def delete_config(self, config_name):
        for c in self.configs:
            if c.name == config_name:
                self.configs.remove(c)
                self.check_storage()
                return c
        self.check_storage()
        return None

    # helpers
    def check_params(self, status, storage_status):
        if status is '' and storage_status is '':
            return True
        elif status is '':
            for s in self.storage_status_enum:
                if s == storage_status:
                    return True
            return False
        elif storage_status is '':
            for s in self.status_enum:
                if s == status:
                    return True
            return False
        return False
