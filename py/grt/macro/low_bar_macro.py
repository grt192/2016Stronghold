from grt.core import GRTMacro
import threading

class LowBarMacro(GRTMacro):

	def __init__(self, shooter, pickup, straight_macro):
		super().__init__()
		self.shooter = shooter
		self.pickup = pickup
		self.straight_macro = straight_macro
		self.timers_running = False
		self.run_autonomous = self.run_threaded
		self.stop_autonomous = self.terminate

	def macro_initialize(self):
		self.timers_running = True
		self.pickup.disable_automatic_control()
		self.pickup.angle_change(.5)
		#self.shooter.turntable.disable_front_lock()
		#self.shooter.turntable.joystick_turn(-.2)
		#threading.Timer(1.0, self.stop_turntable).start()
		threading.Timer(1.8, self.stop_mechs_start_drive).start()

	#def stop_turntable(self):
	#	if self.timers_running:
	#		self.shooter.turntable.joystick_turn(0)


	def stop_mechs_start_drive(self):
		if self.timers_running:
			self.pickup.angle_change(0)
			self.straight_macro.POWER = -.4
			self.straight_macro.set_forward()
			self.straight_macro.enable()
			threading.Timer(4.60, self.stop_drive_start_turn).start()

	def stop_drive_start_turn(self):
		if self.timers_running:
			self.straight_macro.disable()
			self.straight_macro.POWER = -.85
			self.straight_macro.dt.set_dt_output(.4, -.4)
			threading.Timer(2.0, self.stop_turn_start_shot).start()

	def stop_turn_start_shot(self):
		if self.timers_running:
			#self.straight_macro.disable()
			#self.straight_macro.POWER = -.85
			self.straight_macro.dt.set_dt_output(0, 0)
			self.shooter.vt_automatic_shot()
			threading.Timer(6.0, self.stop_shot).start()

	def stop_shot(self):
		if self.timers_running:
			#self.shooter.abort_automatic_shot()
			self.shooter.execute_shot()

	def macro_stop(self):
		self.timers_running = False
		self.straight_macro.disable()
		self.shooter.abort_automatic_shot()
		self.shooter.turntable.disable_front_lock()
		self.shooter.turntable.joystick_turn(0)
		self.straight_macro.POWER = -.85
		self.pickup.angle_change(0)

