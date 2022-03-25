import os
from datetime import datetime
# from Robot.camera import take_images
from Robot.cam_nopyrealsense import take_images
from models.file_entry import FileEntry


# This is an Abstraction of the actual Robot. this can be used to run Test without the robot
def wake_cambot():
    return 'ok'


def take_snapshot(parent_item):
    name = take_images(parent_item)
    size = os.path.getsize(name)
    file = FileEntry('snapshot', name, 'image/png', str(datetime.now()))
    return file, size, 'ok'


def set_home():
    return 'ok'
