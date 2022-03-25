import json


class Position:
    def __init__(self, description, a, y, b):
        self.description = description
        self.a = a
        self.y = y
        self.b = b

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
