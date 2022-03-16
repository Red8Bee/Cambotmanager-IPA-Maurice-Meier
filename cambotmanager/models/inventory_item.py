class InventoryItem:
    def __init__(self, config, id_tag):
        self.id_tag = id_tag
<<<<<<< Updated upstream
        self.storage_status = 'create Enum'
        self.status = "create Enum"
        self.start_date
        self.end_date
        self.config = config
        self.snapshots = []

=======
        self.storage_status = 'floating'
        self.status = 'in_queue'
        self.start_date = None
        self.end_date = None
        self.config = config
        self.snapshots = []
        self.base_directory = base_directory
        self.store_days_left = 30
>>>>>>> Stashed changes
