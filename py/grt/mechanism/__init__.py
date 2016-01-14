class Flywheel:
	def __init__(self, motor):
		self.motor = motor
		self.power = 0
		self.motor.set(self.power)

	def increment(self):
		if self.power >= -.975:
			self.power -= .025
			self.motor.set(self.power)
			print("Power: ", self.power)

	def decrement(self):
		if self.power <= -.025:
			self.power += .025
			self.motor.set(self.power)
			print("Power: ", self.power)
