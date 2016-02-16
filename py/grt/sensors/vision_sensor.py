from grt.core import Sensor


class VisionSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.rotation_error = self.vertical_error = self.target_view = None

    def poll(self):
        pass
