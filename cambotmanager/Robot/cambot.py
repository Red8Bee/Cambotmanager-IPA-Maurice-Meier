# from Robot.camera import take_images
import os

from Robot.cam_nopyrealsense import take_images
from datetime import datetime
import time

from models.file_entry import FileEntry


def wake_cambot(s):
    s.write("\r\n\r\n".encode())
    time.sleep(2)  # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input


def _send_gcode(s, gCode):
    l = gCode.strip()  # Strip all EOL characters for consistency
    print(l)
    s.write((l + '\n').encode())  # Send g-code block to grbl
    while True:
        s.write('$G\n'.encode())
        grbl_out = s.readline()  # Wait for grbl response with carriage return
        decoded = grbl_out.decode('utf-8')
        print(decoded)
        if decoded == '[GC:G0 G54 G17 G21 G90 G94 M5 M9 T0 F0]\r\n':
            return True, 'success'


# checking if coordinates are inside bounds X max:27 min:0 Y max:300 min:1 Z max0 min0
# swap values if Robot configuration gets edited
def _check_bounds(x, y, z):
    if x > 27:
        x = 27
    if x < 0:
        x = 0
    if y > 300:
        y = 300
    if y < 1:
        y = 1
    if z > 0:
        z = 0
    if z < 0:
        z = 0
    return x, y, z


# # Code for camara with pyrealsense2
# def take_snapshot(parent_item, position, s):
#     gcode = 'G00 X' + position.a + ' Y' + position.y + ' Z' + position.b
#     worked, error = _send_gcode(s, gcode)
#     if worked:
#         color_name, depth_name = take_pictures(parent_item)
#         size = os.path.getsize(name)
#         depth_file = FileEntry('depth', depth_name, 'image/png', str(datetime.now()))
#         color_file = FileEntry('color', color_name, 'image/png', str(datetime.now()))
#         files = [color_file, depth_file]
#         return files, size
#     else:
#         return worked, error

def take_snapshot(parent_item, position, s):
    x = position.a
    y = position.y
    z = position.b
    checked_x, checked_y, checked_z = _check_bounds(x, y, z)
    gcode = 'G00 X' + str(checked_x) + ' Y' + str(checked_y) + ' Z' + str(checked_z)
    worked, error = _send_gcode(s, gcode)
    if worked:
        name = take_images(parent_item)
        size = os.path.getsize(name)
        file = FileEntry('color', name, 'image/png', str(datetime.now()))
        return file, size, 'ok'
    else:
        return worked, error


def set_home(s):
    s.write(('$H' + '\n').encode())  # Send g-code block to grbl
    grbl_out = s.readline()  # Wait for grbl response with carriage return
    decoded = grbl_out.decode('utf-8')
    if decoded == 'ok\r\n':
        return True, 'success'
    else:
        return False, 'error'
