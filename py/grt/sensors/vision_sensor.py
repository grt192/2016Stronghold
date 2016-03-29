from grt.core import Sensor


class VisionSensor(Sensor):
    def __init__(self, robot_vision):
        super().__init__()
        self.rotational_error = self.avg_height = self.distance = False
        self.target_view = False
        #False indicates that the target is not in sight

    # self.robot_vision = robot_vision
    def poll(self):
        self.target_view = self.robot_vision.getTargetView()
        
        if self.target_view:
            self.rotational_error = self.robot_vision.getRotationalError()
            self.vertical_error = self.robot_vision.getVerticalError()