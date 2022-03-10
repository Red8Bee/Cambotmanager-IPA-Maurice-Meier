class Status:
    def __init__(self, robot_status, robot_status_code, extended_status_code, disk_available, position):
        self.robot_status = robot_status
        self.robot_status_code = robot_status_code
        self.extended_status_code = extended_status_code
        self.disk_available = disk_available
        self.position = position
        