import threading

class OperationManager:
	def __init__(self, shooter, pickup, straight_macro, record_macro, playback_macro):
		self.op_lock = False
		self.chival_timers_running = False
		self.current_op = "None"
		self.shooter = shooter
		self.pickup = pickup
		self.shooter.operation_manager = self
		self.pickup.operation_manager = self
		self.straight_macro = straight_macro
		self.straight_macro.operation_manager = self
		self.original_straight_macro_power = self.straight_macro.POWER

		self.record_macro = record_macro
		self.playback_macro = playback_macro
		self.playback_macro.operation_manager = self

	def operation(func):
		def self_enable(self):
			if self.op_lock:
				print("Operation bounced!")
				return
			else:
				self.op_lock = True
				self.current_op = func.__name__
				return func(self)
		return self_enable

	def op_abort(func):
		def self_enable(self):
			if "portcullis" in self.current_op and "portcullis" in func.__name__:
				return func(self)
			elif "chival" in self.current_op and "chival" in func.__name__:
				return func(self)
			elif "straight" in self.current_op and "straight" in func.__name__:
				return func(self)
			elif "pickup" in self.current_op and "pickup" in func.__name__:
				return func(self)
			elif "shot" in func.__name__:
				return func(self)
			else:
				print("Abort bounced")
				return
		return self_enable

		#If TT override --> control TT anyway
		#If hood override --> assume hood ready
		#If rails override --> wait for rails actuation
		#If flywheel override --> use voltage control mode
		#If pickup override --> assume pickup ready

	@operation
	#Add logic to check that the pickup arm is down and the elevator rails are raised!
	def vt_automatic_shot(self):
		self.op_lock = True
		self.shooter.vt_automatic_shot()

	@operation	
	def geo_automatic_shot(self):
		self.op_lock = True
		self.shooter.geo_automatic_shot()

	@op_abort
	def shot_abort(self):
		self.shooter.abort_automatic_shot()

	@operation
	def manual_pickup(self):
		self.op_lock = True
		self.shooter.turntable.enable_front_lock()
		self.shooter.rails.rails_up()
		self.pickup.go_to_pickup_position()
		self.pickup.roll(0.5)
		self.shooter.flywheel.spin_to_pickup_power()

	@op_abort
	def manual_pickup_abort(self):
		#Directly controls mechanism functions for manual control mode
		#Will need the mechanism itself to control these functions for automatic pickup
		self.pickup.roll(0)
		self.shooter.flywheel.spindown()
		self.op_lock = False


	@operation
	def chival_cross(self):
		self.op_lock = True
		self.chival_timers_running = True
		self.shooter.drivecontroller.disable_manual_control() #Fix this -- the shooter shouldn't really own a drivecontroller
		self.shooter.rails.rails_down()
		self.shooter.hood.go_to_frame_angle()
		self.shooter.flywheel.spindown()
		self.shooter.turntable.enable_front_lock()
		self.pickup.go_to_pickup_position()
		threading.Timer(.5, self.chival_finish_cross).start()
		#self.chival_macro.enable()

	def chival_finish_cross(self):
		if self.chival_timers_running:
			self.pickup.disable_automatic_control()
			self.playback_macro.start_playback()
		


	@op_abort
	def chival_cross_abort(self):
		#self.chival_macro.disable()
		#self.straight_macro.disable()
		self.playback_macro.stop_playback()
		#self.chival_timers_running = False
		#self.op_lock = False
		#Called when recorded cross finished or aborted

	@operation
	def portcullis_cross(self):
		self.op_lock = True
		print("Running portcullis cross!")
		self.shooter.drivecontroller.disable_manual_control() #Fix this -- the shooter shouldn't really own a drivecontroller
		self.shooter.rails.rails_down()
		self.shooter.hood.go_to_frame_angle()
		self.shooter.flywheel.spindown()
		self.shooter.turntable.enable_front_lock()
		self.pickup.roll(-1.0)
		self.straight_macro.POWER = -.4
		self.straight_macro.enable()

	@op_abort
	def portcullis_cross_abort(self):
		self.straight_macro.disable()
		self.straight_macro.POWER = self.original_straight_macro_power
		self.shooter.drivecontroller.enable_manual_control()
		self.pickup.roll(0)
		self.op_lock = False


	@operation
	def straight_cross(self):
		self.op_lock = True
		self.shooter.drivecontroller.disable_manual_control() #Fix this -- the shooter shouldn't really own a drivecontroller
		self.shooter.rails.rails_down()
		self.shooter.hood.go_to_frame_angle()
		self.shooter.flywheel.spindown()
		self.shooter.turntable.enable_front_lock()
		self.pickup.go_to_cross_position()
		self.straight_macro.enable()
		#Call a straight macro

	def forward_straight_cross(self):
		self.straight_macro.set_forward()
		self.straight_cross()

	def reverse_straight_cross(self):
		self.straight_macro.set_reverse()
		self.straight_cross()

	@op_abort
	def straight_cross_abort(self):
		self.straight_macro.disable()
		self.shooter.drivecontroller.enable_manual_control()
		#self.shooter.drivecontroller.enable_manual_control()
		#self.shooter.abort_automatic_shot()
		self.op_lock = False
		#Called when straight macro aborted (won't finish on its own)

	

	def twirly_cross(self):
		pass

	def twirly_cross_abort(self):
		pass

#op_finished methods should not actually disable the op_lock.
#That should be done by the final mechanism method to run for the operation.
#op_finished methods should be called either in abort portions of the mech controller
#or by the 


#op_finished mehtods should not actually disable the op_lock
#the op_finished methods should really be op_abort methods that pass
#control to the necessary mechanism abort functions
#the proper mechanism finished functions (called in both the abort and normal sequences)
#should disable the op_lock.




