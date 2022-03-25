import unittest

from robot_manager.manager import Manager
from models.inventory_item import InventoryItem


class StorageTests(unittest.TestCase):
    manager = Manager()

    def test_clean(self):
        id_tag = 'f2a1da50-6771-444e-b0e0-86caa747f3be'
        item_to_delete = InventoryItem(None, id_tag, './testFolder')
        item_to_delete.storage_status = 'scheduled_delete'
        self.manager.inventory.all_items.append(item_to_delete)
        all_items_before_clean = self.manager.get_whole_inventory('', '')
        self.manager.storage_handler.clean_inventory()
        all_items_after_clean = self.manager.get_whole_inventory('', '')
        self.assertGreater(len(all_items_before_clean), len(all_items_after_clean), "check if item was deleted")

    def test_add_snapshot(self):
        snapshot_size = 20000
        storage_before_adding = self.manager.storage_handler.size
        self.manager.storage_handler.snapshot_added(snapshot_size)
        storage_after_adding = self.manager.storage_handler.size
        self.assertGreater(storage_after_adding,storage_before_adding, 'Added item to storage')

    # def test_remove_item(self):
