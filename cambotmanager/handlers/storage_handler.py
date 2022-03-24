# this class watches the disc and reserves space for new storage Items
import datetime


class StorageHandler:

    def __init__(self, manager):
        self.max_size = 10000
        self.manager = manager
        self.size = 0

    def clean_inventory(self):
        for item in self.manager.inventory.all_items:
            if item.store_days_left > 0:
                item.storage_status = 'scheduled_delete'
            else:
                now = datetime.datetime.now()
                difrence = now - item.end_date
                days = difrence.days
                item.store_days_left = 30 - days

            if item.storage_status == 'scheduled_delete':
                self.manager.delete_inventory_item(item.id_tag)

    def is_storage_full(self):
        if self.size >= self.max_size:
            return True
        return False

    def snapshot_added(self, snapshot_size):
        self.size = self.size + snapshot_size

    def item_removed(self, item_size):
        self.size = self.size - item_size
