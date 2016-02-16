from wpilib import CANTalon
from grt.core import Sensor


class Hood:
    def __init__(self, robot_vision, hood_motor):
        self.hood_motor = hood_motor
        self.robot_vision = robot_vision

    def go_to_target_angle(self):
        if self.robot_vision.target_view:
            vertical_error = self.robot_vision.vertical_error
            self.deg_set_angle(vertical_error)

    def raw_set_angle(self, value):
        self.hood_motor.changeControlMode(CANTalon.ControlMode.Position)
        self.hood_motor.setP(1)
        self.hood_motor.set(value)

    def deg_set_angle(self, angle):
        # TODO: ADD PROPER CONVERSION CONSTANTS
        self.raw_set_angle(angle)

    # self.hood_motor.set(angle)


class HoodSensor(Sensor):
    ANGLE_TOLERANCE = 5

    def __init__(self, hood):
        super().__init__()
        self.hood = hood

    def poll(self):
        self.vertical_ready = self.hood.hood_motor.getClosedLoopError() < self.ANGLE_TOLERANCE