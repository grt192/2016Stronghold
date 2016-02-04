class ManualTurntable:

	def __init__(self, motor):
		self.motor = motor

	def turn(self, power):
		self.motor.set(power)
		