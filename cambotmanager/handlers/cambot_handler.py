import datetime

import serial

import Robot.cambot as cambot
from models.inventory_item import InventoryItem
from models.config import Config
from models.position import Position
from models.snapshot import Snapshot
from apscheduler.schedulers.background import BackgroundScheduler


def _start_job(statemachine):
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(statemachine, 'interval', seconds=10)
    sched.start()


class CambotHandler:
    def __init__(self, manager):
        # self.s = serial.Serial('COM6', 115200)  # GRBL operates at 115200 baud. Leave that part alone.
        self.state = 0
        self.manager = manager
        self.active_item = None
        self.active_config = None
        _start_job(self.tick)

    def tick(self):
        if self.state == 0:
            self._idle()
        if self.state == 1:
            self._get_item()
        if self.state == 2:
            self._run_config
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
        if type(self.active_item) == InventoryItem and self.active_item.storage_status == 'in_queue':
            self.active_item.storage_status = 'in_progress'
            self.manager.robot_status = 'busy'
            self.state = 2
        else:
            self.state = 0

    # run Config and take Snapshots
    def _run_config(self):
        self._take_all_snapshots()
        self.state = 3

        # return item

    def _return_item(self):
        self.manager.inventory.done.append(self.active_item)
        self.state = 4

    def _home(self):
        cambot.set_home(self.s)
        self.state = 0

    # helpers
    def _take_all_snapshots(self, position: Position):
        cambot.wake_cambot(self.s)
        cambot.set_home(self.s)
        files, size = cambot.take_snapshot(self.active_item.base_directory, position, self.s)
        is_last_snapshot = self._check_if_last()
        snapshot = Snapshot(datetime.datetime.now(), files, position, size, is_last_snapshot)
        self.active_item.snapshots.append(snapshot)
        if not is_last_snapshot:
            all_positions = self.active_config.positions
            index = all_positions.index(position)
            next_index = index + 1
            next_position = all_positions[next_index]
            self._take_all_snapshots(next_position)

    def _check_if_last(self, position: Position):
        all_positions = self.active_item.config.positions
        index = all_positions.index(position)
        length = len(all_positions)
        if index + 1 == length:
            return True
        return False
