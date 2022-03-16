from datetime import datetime

from models.file_entry import FileEntry


def wake_cambot():
    return 'ok'


def take_snapshot():
    color_name = '../Inventory/test_images/color.png'
    depth_name = '../Inventory/test_images/depth.png'
    size = 30000
    depth_file = FileEntry('depth', depth_name, 'image/png', datetime.now())
    color_file = FileEntry('color', color_name, 'image/png', datetime.now())
    files = [color_file, depth_file]
    return files, size


def set_home(s):
    return 'ok'
