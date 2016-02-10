class Pickup:

	def __init__(self, achange_motor_1, achange_motor_2, roller_motor):
		self.achange_motor_1 = achange_motor_1
		self.achange_motor_2 = achange_motor_2
		self.roller_motor = roller_motor

	def angle_change(self, power):
		#self.achange_motor_1.set(power)
		self.achange_motor_2.set(power)

	def roll(self, power):
		self.roller_motor.set(power)
	def stop(self):
		self.roller_motor.set(0)

	def set_automatic(self):
		#self.achange_motor_1.changeControlMode(CANTalon.ControlMode.Position)
		self.achange_motor_2.changeControlMode(CANTalon.ControlMode.Position)

	def set_manual(self):
		#self.achange_motor_1.changeControlMode(CANTalon.ControlMode.PercentVbus)
		self.achange_motor_2.changeControlMode(CANTalon.ControlMode.PercentVbus)

	def zero(self):
		set_automatic()
		#self.achange_motor_1.setSensorPosition(0)
		self.achange_motor_2.setSensorPosition(0)

	def go_to_zero(self):
		set_automatic()
		#self.achange_motor_1.set(0)
		self.achange_motor_2.set(0)

	def go_back(self):
		set_automatic()
		#self.achange_motor_1.set(2700)
		self.achange_motor_2.set(-2700)

	def go_to_portcullis(self):
		set_automatic()
		#self.achange_motor_1.set(500)
		self.achange_motor_2.set(-500)