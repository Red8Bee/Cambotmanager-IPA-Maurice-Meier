import datetime

import serial
import time

from models.file_entry import FileEntry
from models.inventory_item import InventoryItem
from models.config import Config
from  models.position import Position
from models.snapshot import Snapshot


def _wake_cambot(s):
    s.write("\r\n\r\n".encode())
    time.sleep(2)  # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input

def _send_gcode(s, gCode):
    l = gCode.strip()  # Strip all EOL characters for consistency
    print('Sending: ' + l)
    s.write((l + '\n').encode())  # Send g-code block to grbl
    grbl_out = s.readline()  # Wait for grbl response with carriage return
    print(' : ' + (grbl_out.strip()).decode())

def _take_snapshot(snapshot):
    gcode = 'G00 X' + snapshot.position.a + ' Y' + snapshot.position.y + ' Z' + snapshot.position.b
    _send_gcode(gcode)
    color_name, depth_name, size = _take_pictures(snapshot)
    depth_file = FileEntry('depth', None, 'image/jpeg', datetime.datetime.now())
    color_file = FileEntry('color', None, 'image/jpeg', datetime.datetime.now())
    files = [color_file, depth_file]
    return files, size

def _take_pictures():


    return color_name, depth_name, size

def set_home(s):
    _send_gcode('$H')

class CambotHandler:
    def __init__(self, manager):
        # Open grbl serial port ==> CHANGE THIS BELOW TO MATCH YOUR USB LOCATION
        self.s = serial.Serial('COM6', 115200)  # GRBL operates at 115200 baud. Leave that part alone.
        _wake_cambot(self.s)
        self.state = 0
        self.manager = manager
        self.active_item = None
        self.active_config = None


    def tick(self):
        if self.state == 0:
            self._idle()
        if self.state == 1:
            self._get_item()
        if self.state == 2:
            self._get_config()
        if self.state == 3:
           self._create_snapshot()
        if self.state == 4:
            # return Item
        if self.state == 5:
            # home
        if self.state == 6:
            #error

# wait for new Item or snapshot
    def _idle(self):
        if len(self.manager.inventory.todo) > 0:
            self.state = 1

# get item from manager
    def _get_item(self):
        self.active_item = self.manager.inventory.todo[0]
        if type(self.active_item) == InventoryItem:
            self.state = 2

# get config from item
    def _get_config(self):
        self.active_config = self.active_item.config
        if type(self.active_config ) == Config:
            self.state = 3

# create snapshot
    def _create_snapshot(self):
        snapshotcount = len(self.active_item.snapshots)
        position = self.active_config.positions[snapshotcount]
        active_snapshot = Snapshot(datetime.datetime.now(),None,position,None,False)
        files, size = _take_snapshot(active_snapshot)
        active_snapshot.files = files
        active_snapshot.size = size
        if snapshotcount == len(self.active_config.positions):
            active_snapshot.last_snapshot = True
        self.active_item.snapshots.append(active_snapshot)
        self.state = 4
# return item
    def _return_item(self):
        self.manager.inventory.done.append(self.active_item)
        self.state = 5

    def _home(self):
        set_home()
        self.state = 0


