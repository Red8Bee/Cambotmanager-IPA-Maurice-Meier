import json


class InventoryItem:
    def __init__(self, config, id_tag, base_directory):
        self.id_tag = id_tag
        self.storage_status = 'floating'
        self.status = 'in_queue'
        self.start_date = None
        self.end_date = None
        self.config = config
        self.snapshots = []
        self.base_directory = base_directory
        self.store_days_left = 30

    def toJSON(self):
        # json_config = self.config.toJSON()
        # json_snapshots = []
        # for s in self.snapshots:
        #     json_snapshots.append(s.toJSON)
        #
        # json_item = InventoryItem(json_config, self.id_tag, self.base_directory)
        # json_item.storage_status = self.storage_status
        # json_item.status = self.status
        # json_item.start_date = self.start_date
        # json_item.end_date = self.end_date
        # json_item.store_days_left = self.store_days_left
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
