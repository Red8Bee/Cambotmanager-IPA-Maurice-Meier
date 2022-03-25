import json


class Inventory:
    def __init__(self):
        self.all_items = []
        self.todo = []
        self.done = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
