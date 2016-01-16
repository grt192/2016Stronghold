from wpilib import CANTalon


class VisionMechanism:
	#Actually the shooter?
	def __init__(self, vision_sensor, dt_left, dt_right):
		self.vision_sensor = vision_sensor
		self.vision_enabled = False

		self.dt_left = dt_left
		self.dt_right = dt_right

		self.target_acquired = False

		self.setpoint = 0 #Zero error is dead-center in the camera's field of view
		#Either make sure this works with settings other than zero or make sure the camera is mounted
		#in the exact center (x-axis) of the shooter

		self.dt_left.changeControlMode(CANTalon.ControlMode.Position)
		self.dt_left.setP(1)
		self.dt_right.changeControlMode(CANTalon.ControlMode.Position)
		self.dt_right.setP(1)

		self.dt_left.set(self.setpoint)
		self.dt_right.set(self.setpoint)
		self.vision_sensor.add_listener(self._vision_listener)

	def override_dt_outputs(self):
		pass

	def spinup(self):
		pass

	def launch(self):
		pass

	def _vision_listener(self, sensor, state_id, datum):
		#print("Listener running")
		#print(state_id)
		if self.vision_enabled:
			self.spinup()
			if state_id == "rotational_error":
				if datum:
					print("Rotation error: ", datum)
					self.override_dt_outputs()

					

					self.dt_left.setSensorPosition(datum)
					self.dt_right.setSensorPosition(datum)
					print(self.dt_left.getEncPosition())

					if self.dt_left.getOutputVoltage() < 1 and self.dt_right.getOutputVoltage() < 1: #Should trigger when the motors are virtually stopped
						self.target_acquired = True

					#Make sure the vision processing code filters out octagons with far too small of an area
					#Use robot camera values, not computer camera values

					#PID Controller magic
			elif state_id == "avg_height":
				if datum:
					print("Average height: ", datum)
			elif state_id == "distance":
				if datum:
					print("Distance: ", datum)
					if self.target_acquired:
						self.launch()

