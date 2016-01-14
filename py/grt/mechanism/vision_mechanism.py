
class VisionMechanism:
	#Actually the shooter?
	def __init__(self, vision_sensor):
		self.vision_sensor = vision_sensor
		self.vision_enabled = True
		self.vision_sensor.add_listener(self._vision_listener)

	def _vision_listener(self, sensor, state_id, datum):
		#print("Listener running")
		print(state_id)
		if self.vision_enabled:
			if state_id == "rotational_error":
				if datum:
					print("Rotation error: ", datum)
					#PID Controller magic
			elif state_id == "avg_height":
				if datum:
					print("Average height: ", datum)
			elif state_id == "distance":
				if datum:
					print("Distance: ", datum)