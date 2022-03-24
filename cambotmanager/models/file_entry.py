import json


class FileEntry:
    def __init__(self, image_type, file_name, mime, time):
        self.image_type = image_type
        self.file_name = file_name
        self.mime = mime
        self.time = time

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
