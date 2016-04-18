
class Rails:
	def __init__(self, shooter):
		self.shooter = shooter
		self.rails_actuator = shooter.rails_actuator
		self.shooter_act = self.rails_actuator
		self.current_position = "down"

	def rails_up(self):
		self.current_position = "up"
		self.rails_actuator.set(True)
	def rails_down(self):
		self.current_position = "down"
		self.rails_actuator.set(False)
