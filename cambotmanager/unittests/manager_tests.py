import unittest

from robot_manager.manager import Manager
from models.config import Config
from models.inventory_item import InventoryItem


class ManagerTests(unittest.TestCase):
    manager = Manager()
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
