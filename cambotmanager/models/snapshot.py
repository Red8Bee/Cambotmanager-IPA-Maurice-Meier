import json


class Snapshot:
    def __init__(self, time, files, position, size, last_snapshot):
        self.time = str(time)
        self.success = "ok_scheduled"
        self.files = files
        self.position = position
        self.size = size
        self.last_snapshot = last_snapshot

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
