from wpilib import CANTalon
from grt.core import Sensor


class Hood:
    def __init__(self, robot_vision, hood_motor):
        self.hood_motor = hood_motor
        self.robot_vision = robot_vision

    def go_to_target_angle(self):
        if self.robot_vision.target_view:
            self.auto_set(self.get_target_angle(self.robot_vision.vertical_error))

    def get_target_angle(self, vertical_error):
        # TODO: Add conversion constants

        return vertical_error

    def go_to_standby_angle(self):
        self.auto_set(1000)

    def go_to_frame_angle(self):
        self.auto_set(0)

    def go_to_geo_angle(self):
        self.auto_set(1000)

    def auto_set(self, angle):
        if not self.hood_motor.getControlMode == CANTalon.ControlMode.PercentVbus:
            self.hood_motor.set(angle)

    def rotate(self, power):
        if self.hood_motor.getControlMode() == CANTalon.ControlMode.PercentVbus:
            self.hood_motor.set(-power)
        else:
            print("Hood motor not in PercentVbus control mode!")

    def enable_automatic_control(self):
        self.hood_motor.changeControlMode(CANTalon.ControlMode.Position)
        self.hood_motor.setP(.01)  # TODO: MAGIC NUMBER

    def disable_automatic_control(self):
        self.hood_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)


# class HoodSensor(Sensor):
# 	ANGLE_TOLERANCE = 5
#
# 	def __init__(self, hood):
# 		super().__init__()
# 		self.hood = hood
#
# 	def poll(self):
# 		if self.hood.hood_motor.getControlMode() == CANTalon.ControlMode.PercentVbus:
# 			self.vertical_ready = True
# 		else:
# 			if self.hood.hood_motor.getClosedLoopError() < self.ANGLE_TOLERANCE:
# 				self.vertical_ready = True
# 			else:
# 				self.vertical_ready = False
#
#
#
