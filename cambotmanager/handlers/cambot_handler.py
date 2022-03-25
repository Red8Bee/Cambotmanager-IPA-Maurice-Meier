import datetime

import serial

import Robot.cambot as cambot
import Robot.cambot_test_robot as test_cambot
from models.inventory_item import InventoryItem
from models.config import Config
from models.position import Position
from models.snapshot import Snapshot
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def _add_metadata_file(item):
    directory = item.base_directory
    iso_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = item.id_tag + '---snapshots---' + iso_timestamp + '---metadata.ini'
    whole_path = directory + '/' + file_name
    position_string = ''
    for position in item.config.positions:
        string = 'A: ' + str(position.a) + ',Y: ' + str(position.y) + ',B: ' + str(position.b)
        position_string = position_string + ';' + string
    f = open(whole_path, 'w')
    f.write("Status: " + item.status + '\n'+ "Positions:" + position_string)
    f.close()


class CambotHandler:
    def __init__(self, manager):
        self.s = serial.Serial('COM6', 115200)  # GRBL operates at 115200 baud. Leave that part alone.
        self.state = 0
        self.manager = manager
        self.active_item = None
        self.active_config = None

    def reset(self):
        cambot.set_home(self.s)
        # test_cambot.set_home()

    def tick(self):
        print('tick')
        if self.state == 0:
            self._idle()
        if self.state == 1:
            self._get_item()
        if self.state == 2:
            self._run_config()
        if self.state == 3:
            self._return_item()
        if self.state == 4:
            self._home()
        if self.state == 5:
            return

    # wait for new Item or snapshot
    def _idle(self):
        self.manager.robot_status = 'idle'
        if len(self.manager.inventory.todo) > 0:
            self.state = 1

    # get item from robot_manager
    def _get_item(self):
        self.active_item = self.manager.inventory.todo[0]
        if type(self.active_item) == InventoryItem and self.active_item.status == 'in_queue':
            self.active_item.storage_status = 'in_progress'
            self.active_item.start_date = datetime.now()
            self.manager.robot_status = 'busy'
            self.active_config = self.active_item.config
            self.active_config.is_in_use = True
            self.manager.stop_scheduler()
            self.state = 2
        else:
            self.state = 0

    # run Config and take Snapshots
    def _run_config(self):
        all_snapshots_taken = self._take_all_snapshots()
        if all_snapshots_taken:
            self.state = 3
        else:
            self.manager.restart_scheduler()
            self.state = 0

        # return item

    def _return_item(self):
        self.manager.inventory.done.append(self.active_item)
        self.manager.inventory.todo.remove(self.active_item)
        self.active_item.end_date = datetime.now()
        _add_metadata_file(self.active_item)
        self.state = 4

    def _home(self):
        cambot.set_home(self.s)
        # test_cambot.set_home()
        self.manager.restart_scheduler()
        self.state = 0

    # helpers
    def _take_all_snapshots(self):
        cambot.wake_cambot(self.s)
        worked, status = cambot.set_home(self.s)
        # test_cambot.wake_cambot()
        # worked, status = test_cambot.set_home()
        snapshot_count = 0
        all_positions = self.active_config.positions
        if worked:
            while True:
                position = all_positions[snapshot_count]
                # files, size, status = test_cambot.take_snapshot(self.active_item)
                files, size, status = cambot.take_snapshot(self.active_item, position, self.s)
                if status == 'ok':
                    is_last_snapshot = self._check_if_last(position)
                    snapshot = Snapshot(datetime.now(), files, position, size, is_last_snapshot)
                    self.active_item.snapshots.append(snapshot)
                    snapshot_count = snapshot_count + 1
                else:
                    self.handle_robot_error()
                    return False
                if is_last_snapshot:
                    self.active_item.status = 'success'
                    return True
        else:
            self.handle_robot_error()
            return False

    def _check_if_last(self, position: Position):
        all_positions = self.active_item.config.positions
        index = all_positions.index(position)
        length = len(all_positions)
        if index + 1 == length:
            return True
        return False

    def handle_robot_error(self):
        self.manager.status.robot_status = 'error'
        self._home()
        self.active_item.status = 'fail'
