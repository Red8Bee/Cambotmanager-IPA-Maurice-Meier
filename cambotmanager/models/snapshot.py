class Snapshot:
    def __init__(self, time, files, position, size, last_snapshot):
        self.time = time
        self.success = "emum"
        self.files = files
        self.position = position
        self.size = size
        self.last_snapshot = last_snapshot
