from Robot.camera import take_images
from datetime import datetime, time

from models.file_entry import FileEntry


def wake_cambot(s):
    s.write("\r\n\r\n".encode())
    time.sleep(2)  # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input


def _send_gcode(s, gCode):
    l = gCode.strip()  # Strip all EOL characters for consistency
    s.write((l + '\n').encode())  # Send g-code block to grbl
    grbl_out = s.readline()  # Wait for grbl response with carriage return
    decoded = grbl_out.decode('utf-8')
    if decoded == 'ok':
        return True, 'success'
    else:
        return False, decoded


def take_snapshot(position, base_directory, s):
    gcode = 'G00 X' + position.a + ' Y' + position.y + ' Z' + position.b
    worked, error = _send_gcode(s, gcode)
    if worked:
        color_name, depth_name, size = take_pictures(base_directory)
        depth_file = FileEntry('depth', depth_name, 'image/png', datetime.now())
        color_file = FileEntry('color', color_name, 'image/png', datetime.now())
        files = [color_file, depth_file]
        return files, size
    else:
        return worked, error


def take_pictures(base_directory):
    color_name, depth_name, size = take_images(base_directory)
    return color_name, depth_name, size


def set_home(s):
    _send_gcode(s, '$H')
