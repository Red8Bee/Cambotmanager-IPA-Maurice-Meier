import json


class Config:
    def __init__(self, name, description, image_type, positions, default_max_progress):
        self.name = name
        self.description = description
        self.image_type = image_type
        self.positions = positions
        self.default_max_progress = default_max_progress
        self.is_in_use = False

    def toJSON(self)
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)