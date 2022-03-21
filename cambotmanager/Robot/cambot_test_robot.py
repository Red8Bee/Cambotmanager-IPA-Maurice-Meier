from datetime import datetime

# from Robot.camera import take_images
from Robot.cam_nopyrealsense import take_images

from models.file_entry import FileEntry


def wake_cambot():
    return 'ok'


def take_snapshot(parent_item):
    name, size = take_images(parent_item)
    file = FileEntry('snapshot', name, 'image/png', str(datetime.now()))
    return file, size, 'ok'


def set_home():
    return 'ok'
