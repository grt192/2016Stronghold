from grt.core import Sensor

class VisionSensor(Sensor):
	def __init__(self):
		super().__init__()
		self.rotation_error = self.avg_height = self.distance = None
		#self.robot_vision = robot_vision
	def poll(self):
		pass
	#def poll(self):
	#	if self.robot_vision.rotation_locked:
			#Rotation
	#	self.rotation_error
