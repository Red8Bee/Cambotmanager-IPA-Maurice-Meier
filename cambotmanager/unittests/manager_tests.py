import unittest

from robot_manager.manager import Manager
from models.config import Config
from models.inventory_item import InventoryItem


class ManagerTests(unittest.TestCase):
    manager = Manager()

# Inventory_Item
    def test_create_item(self):
        id_tag = 'f2a1da50-6771-444e-b0e0-86caa747f3be'
        config = Config(None, None, None, None, None)
        self.manager.create_inventory_item(config, id_tag)
        list = self.manager.inventory.all_items
        self.assertEqual(len(list), 1, 'is there one Item in the List')

    def test_get_item(self):
        id_tag = 'f2a1da50-6771-444e-b0e0-86caa747f3be'
        config = Config(None, None, None, None, None)
        self.manager.create_inventory_item(config, id_tag)
        item: InventoryItem = self.manager.get_inventory_item(id_tag)
        self.assertEqual(item.id_tag, id_tag, "are id's the same")

    def test_delete_item(self):
        id_tag = 'f2a1da50-6771-444e-b0e0-86caa747f3be'
        config = Config(None, None, None, None, None)
        self.manager.create_inventory_item(config, id_tag)
        list_before_delete = self.manager.inventory.all_items
        self.manager.delete_inventory_item(id_tag)
        list_after_delete = self.manager.inventory.all_items
        self.assertEqual(len(list_after_delete), len(list_before_delete), 'was Item deleted')

# config
    def test_create_config(self):
        json = {
          "name": "d290f1ee-6c54-4b01-90e6-d701748f0851",
          "description": "hyperlapse shot of 1h duration",
          "type": "set",
          "positions": [
            {
              "a": 0,
              "y": 0,
              "b": 0
            }
          ],
          "defaultMaxProgress": 1
        }
        self.manager.create_config(json)
        config = self.manager.get_config(json["name"])
        self.assertEqual(json["name"], config.name)

    def test_delete_config(self):
        conf_name = "d290f1ee-6c54-4b01-90e6-d701748f0851"
        self.manager.delete_config(conf_name)
        config = self.manager.get_config(conf_name)
        self.assertEqual(config, None)
