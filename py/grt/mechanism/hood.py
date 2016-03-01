from wpilib import CANTalon
from grt.core import Sensor

FRAME_POSITION = 155
VT_POSITION = 271
BATTER_POSITION = 200

class Hood:
    HOOD_MIN = 155
    HOOD_MAX = 385
    CURRENT_MAX = 30

    def __init__(self, robot_vision, hood_motor):
        self.hood_motor = hood_motor
        self.robot_vision = robot_vision
        self.override_manager = None




    def go_to_vt_angle(self):
        self.auto_set(VT_POSITION)

    def go_to_geo_angle(self):
        self.auto_set(BATTER_POSITION)

    def go_to_frame_angle(self):
        self.auto_set(FRAME_POSITION)

    def auto_set(self, angle):
        if not self.hood_motor.getControlMode() == CANTalon.ControlMode.PercentVbus:
            self.hood_motor.set(angle)

    def rotate(self, power):
        if self.hood_motor.getOutputCurrent() < self.CURRENT_MAX:
            if self.hood_motor.getControlMode() == CANTalon.ControlMode.PercentVbus:
                self.hood_motor.set(power)
            else:
                print("Hood motor not in PercentVbus control mode!")

    def enable_automatic_control(self):
        if not self.override_manager.hood_override:
            self.hood_motor.changeControlMode(CANTalon.ControlMode.Position)

    def disable_automatic_control(self):
        self.hood_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.hood_motor.set(0)


class HoodSensor(Sensor):
    ANGLE_TOLERANCE = 5

    def __init__(self, hood):
        super().__init__()
        self.hood = hood

    def poll(self):
        if self.hood.hood_motor.getControlMode() == CANTalon.ControlMode.PercentVbus:
            self.vertical_ready = True
        else:
            if self.hood.hood_motor.getClosedLoopError() < self.ANGLE_TOLERANCE:
                self.vertical_ready = True
            else:
                self.vertical_ready = False



