from wpilib import CANTalon
from grt.core import Sensor


class Hood:
	def __init__(self, shooter):
		self.shooter = shooter
		self.hood_motor = shooter.hood_motor
		self.robot_vision = shooter.robot_vision

	def go_to_target_angle(self):
		if self.robot_vision.get_target_view():
			self.deg_set_angle(self.robot_vision.get_target_angle())

	def raw_set_angle(self, value):
		self.hood_motor.changeControlMode(CANTalon.ControlMode.Position)
		self.hood_motor.setP(1)
		self.hood_motor.set(value)
	def deg_set_angle(self, angle):
		#ADD PROPER CONVERSION CONSTANTS
		self.raw_set_angle(angle)
		#self.hood_motor.set(angle)

class HoodSensor(Sensor):
	ANGLE_TOLERANCE = 5

	def __init__(self, hood):
		super().__init__()
		self.hood = hood

	def poll(self):
		if self.hood.hood_motor.getClosedLoopError() < self.ANGLE_TOLERANCE:
			self.vertical_ready = True
		else:
			self.vertical_ready = False