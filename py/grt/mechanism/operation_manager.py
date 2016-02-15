

class OperationManager:
	def __init__(self, shooter, pickup, straight_macro):
		self.op_lock = False
		self.current_op = "None"
		self.shooter = shooter
		self.pickup = pickup
		self.shooter.operation_manager = self
		self.pickup.operation_manager = self
		self.straight_macro = straight_macro
		self.straight_macro.operation_manager = self

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
			if "cross" in self.current_op and "cross" in func.__name__:
				return func(self)
			elif "pickup" in self.current_op and "pickup" in func.__name__:
				return func(self)
			elif "shot" in self.current_op and "shot" in func.__name__:
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
	def automatic_pickup_shot_abort(self):
		self.pickup.abort_automatic_pickup()
		self.shooter.abort_automatic_shot()

	@operation
	def automatic_pickup(self):
		self.op_lock = True
		self.pickup.automatic_pickup()
		self.shooter.automatic_pickup()


	@operation
	def cross_pickup_out(self):
		self.op_lock = True
		self.pickup.go_to_pickup_position()
		self.shooter.rails.rails_down()

	@operation
	def cross_pickup_in(self):
		self.op_lock = True
		self.shooter.rails.rails_down()
		#Delay before doing this
		self.pickup.go_to_frame_position()

	@op_abort
	def cross_abort(self):
		self.shooter.abort_automatic_shot()
		#Check that more specialized logic is not needed

	@operation
	def chival_cross(self):
		pass
		#Run recorded chival de fris cross operation

	@op_abort
	def chival_cross_abort(self):
		self.op_lock = False
		#Called when recorded cross finished or aborted

	@operation
	def straight_cross(self):
		self.op_lock = True
		self.shooter.drivecontroller.disable_manual_control() #Fix this -- the shooter shouldn't really own a drivecontroller
		self.shooter.rails.rails_down()
		self.straight_macro.enable()
		#Call a straight macro

	@op_abort
	def straight_cross_abort(self):
		self.straight_macro.disable()
		self.shooter.drivecontroller.enable_manual_control()
		self.shooter.abort_automatic_shot()
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




