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
