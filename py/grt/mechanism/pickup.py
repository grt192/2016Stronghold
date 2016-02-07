class Pickup:

	def __init__(self, achange_motor_1, achange_motor_2, roller_motor, flywheel_motor):
		self.operation_manager = None
		self.achange_motor_1 = achange_motor_1
		self.achange_motor_2 = achange_motor_2
		self.roller_motor = roller_motor
		self.flywheel_motor = flywheel_motor

	def angle_change(self, power):
		self.achange_motor_1.set(power)
		self.achange_motor_2.set(-power)

	def roll(self, power):
		self.roller_motor.set(power)
	def stop(self):
		self.roller_motor.set(0)

	def automatic_pickup(self):
		self.go_to_pickup_position()
		self.roll(1)

	def abort_automatic_pickup(self):
		self.roll(0)

	def go_to_pickup_position(self):
		pass

	def go_to_frame_position(self):
		pass

	#Pass this the actual flywheel class, eventually.