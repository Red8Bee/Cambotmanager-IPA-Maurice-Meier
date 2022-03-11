import os.path
import shutil

from manager.cambot_handler import CambotHandler
from models.inventory import Inventory
from models.inventory_item import InventoryItem
from models.config import Config
import re


# from .storage_handler import StorageHandler


def create_folder(base_directory_path):
    if not (os.path.exists(base_directory_path)):
        os.mkdir(base_directory_path)


def remove_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)


class Manager:
    # This class handles the communication between robot/storage and API, serves data to the API
    def __init__(self):
        self.cambot_handler = CambotHandler(self)
        # self.storage_handler = StorageHandler()
        self.inventory = Inventory()
        self.configs = []
        self.status_enum = ['success', 'fail', 'in_progress']
        self.storage_status_enum = ['all', 'scheduled_delete', 'stored', 'floating']

    # status
    def get_status(self):
        status = "not implemented"
        return status

    def reset_cambot(self):
        status = "not implemented"
        return status

    # Inventory
    def create_inventory_item(self, config, id_tag):
        base_directory = './Inventory/' + id_tag + '/'
        item = InventoryItem(config, id_tag, base_directory)
        create_folder(base_directory)
        self.inventory.todo.append(item)
        self.cambot_handler.tick()

    def get_whole_inventory(self, status, storage_status):
        params_are_ok = self.check_params(status, storage_status)
        if params_are_ok:
            whole_inventory = self.inventory.todo + self.inventory.done
            searched_inventory = []
            for item in whole_inventory:
                if status is not None and item.status == status:
                    searched_inventory.append(item.id_tag)
                elif storage_status is not None and item.storage_status == storage_status:
                    searched_inventory.append(item.id_tag)
                else:
                    searched_inventory.append(item.id_tag)
            return searched_inventory
        return None

    def get_inventory_item(self, id_tag):
        if self.check_if_id_is_UUID(id_tag):
            whole_inventory = self.inventory.todo + self.inventory.done
            for item in whole_inventory:
                if item.id_tag == id_tag:
                    return item
            return None
        return 'id_invalid'

    def delete_inventory_item(self, id_tag):
        if self.check_if_id_is_UUID(id_tag):
            for item in self.inventory.todo:
                if item.id_tag == id_tag:
                    self.inventory.todo.remove(item)
                    remove_folder(item.base_directory)
                    return item
            for item in self.inventory.done:
                if item.id_tag == id_tag:
                    self.inventory.done.remove(item)
                    remove_folder(item.base_directory)
                    return item
            return None
        return 'id_invalid'

    def get_snapshot_from_item(self, id_tag, snapshot_time):
        item = self.get_inventory_item(id_tag)
        if item != "id_invalid":
            for s in item.snapshots:
                if s.time == snapshot_time:
                    return s
            return None
        return item

    # Config
    def create_config(self, json):
        try:
            config = Config(json['name'], json['description'], json['type'], json['positions'],
                            json['defaultMaxProgress'])
            self.configs.append(config)
            return True
        except ValueError:
            return False

    def get_config(self, config_id):
        for c in self.configs:
            if c.name == config_id:
                return c
        return None

    def get_all_configs(self):
        all_configs = []
        for c in self.configs:
            all_configs.append(c.name)
        return all_configs

    def delete_config(self, config_name):
        for c in self.configs:
            if c.name == config_name:
                self.configs.remove(c)
                return c
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

    def check_if_id_is_UUID(self, id_to_check):
        UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)
        if UUID_PATTERN.match(id_to_check):
            return True
        else:
            return False
