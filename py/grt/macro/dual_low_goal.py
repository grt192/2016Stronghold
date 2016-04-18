from grt.core import GRTMacro
import threading



class DualLowGoal(GRTMacro):

	def __init__(self, shooter, pickup, straight_macro, new_turn_macro):
		super().__init__()
		self.shooter = shooter
		self.pickup = pickup
		self.straight_macro = straight_macro
		self.new_turn_macro = new_turn_macro
		self.timers_running = False
		self.run_autonomous = self.run_threaded
		self.stop_autonomous = self.terminate

	def macro_initialize(self):
		self.timers_running = True
		self.pickup.disable_automatic_control()
		self.pickup.angle_change(.5)
		self.straight_macro.POWER = -.4
		self.straight_macro.set_forward()
		self.straight_macro.enable()
		#threading.Timer(1.8, self.pickup_ready).start()
		threading.Timer(1.8, self.low_bar_clear).start()


	def low_bar_clear(self):
		if self.timers_running:
			self.pickup.disable_automatic_control()
			self.pickup.angle_change(-.5)
			self.straight_macro.POWER = -.85 #Careful of a possible race condition / threading problem
			#threading.Timer(1.8, self.pickup_ready).start()
			threading.Timer(1.8, self.stop_drive_start_turn).start()

	def pickup_ready(self):
		if self.timers_running:
			self.pickup.disable_automatic_control()
			self.pickup.angle_change(0)

	def stop_drive_start_turn(self):
		if self.timers_running:
			self.straight_macro.disable()
			self.pickup.angle_change(0)
			#self.straight_macro.POWER = -.85
			#self.pickup.angle_change(0)
			self.new_turn_macro.set_setpoint(self.new_turn_macro.navx.fused_heading + 30)
			self.new_turn_macro.enable()
			threading.Timer(4, self.shoot_low).start()

	def shoot_low(self):
		if self.timers_running:
			self.new_turn_macro.disable()
			self.shooter.low_automatic_shot()
			threading.Timer(2.0, self.turn_around_prepare_mechs).start()

	def turn_around_prepare_mechs(self):
		if self.timers_running:
			self.shooter.rails.rails_down()
			self.pickup.disable_automatic_control()
			self.pickup.angle_change(-.5)
			threading.Timer(1.8, self.pickup_ready).start()
			self.new_turn_macro.set_setpoint(self.new_turn_macro.navx.fused_heading + 150)
			self.new_turn_macro.enable()
			threading.Timer(4, self.re_cross).start()

	def re_cross(self):
		if self.timers_running:
			self.new_turn_macro.disable()
			self.straight_macro.POWER = -.4
			self.straight_macro.enable()
			self.pickup.roll(.5)
			threading.Timer(4.50, self.stop_re_cross_start_turn).start()

	def stop_re_cross_start_turn(self):
		if self.timers_running:
			self.pickup.roll(0)
			self.straight_macro.disable()
			self.straight_macro.POWER = -.85
			self.new_turn_macro.set_setpoint(0)
			self.new_turn_macro.enable()
			threading.Timer(1.2, self.second_drive_cross).start()

	def second_drive_cross(self):
		if self.timers_running:
			#self.pickup.angle_change(0)
			self.new_turn_macro.disable()
			self.straight_macro.POWER = -.4
			self.straight_macro.set_forward()
			self.straight_macro.enable()
			threading.Timer(3.00, self.second_low_bar_clear).start()

	def second_low_bar_clear(self):
		if self.timers_running:
			#self.pickup.disable_automatic_control()
			#self.pickup.angle_change(-.5)
			self.straight_macro.POWER = -.85 #Careful of a possible race condition / threading problem
			#threading.Timer(1.8, self.pickup_ready).start()
			threading.Timer(1.2, self.second_stop_drive_start_turn).start()


	def second_stop_drive_start_turn(self):
		if self.timers_running:
			self.straight_macro.disable()
			self.straight_macro.POWER = -.85
			#self.pickup.angle_change(0)
			self.new_turn_macro.set_setpoint(30)
			self.new_turn_macro.enable()
			threading.Timer(1.2, self.second_shoot_low).start()

	def second_shoot_low(self):
		if self.timers_running:
			self.new_turn_macro.disable()
			self.shooter.low_automatic_shot()




	def macro_stop(self):
		self.timers_running = False
		self.straight_macro.disable()
		self.straight_macro.POWER = -.85
		self.new_turn_macro.disable()
		self.new_turn_macro.set_setpoint(0)
		self.pickup.angle_change(0)
		self.pickup.roll(0)
		self.shooter.abort_automatic_shot()

