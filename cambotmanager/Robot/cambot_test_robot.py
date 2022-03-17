from datetime import datetime

from Robot.camera import take_images
from models.file_entry import FileEntry


def wake_cambot():
    return 'ok'


def take_snapshot(parent_item):
    color_name, depth_name, size = take_images(parent_item)
    depth_file = FileEntry('depth', depth_name, 'image/png', str(datetime.now()))
    color_file = FileEntry('color', color_name, 'image/png', str(datetime.now()))
    files = [color_file, depth_file]
    return files, size, 'ok'


def set_home():
    return 'ok'
