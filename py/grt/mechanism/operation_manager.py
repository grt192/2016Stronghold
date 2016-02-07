

class OperationManager:
	def __init__(self, shooter):
		self.op_lock = False
		self.shooter = shooter
		self.shooter.op_lock = self.op_lock
		self.pickup.op_lock = self.op_lock

	def operation(self, func):
		if self.op_lock:
			return
		else:
			self.op_lock = True
			return func(self)

		#If TT override --> control TT anyway
		#If hood override --> assume hood ready
		#If rails override --> wait for rails actuation
		#If flywheel override --> use voltage control mode
		#If pickup override --> assume pickup ready

	@operation
	def vt_automatic_shot(self):
		self.op_lock = True
		self.shooter.start_automatic_shot()

	@operation	
	def geo_automatic_shot(self):
		self.op_lock = True
		self.shooter.start_geometric_shot()

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

	def cross_abort(self):
		self.shooter.abort_automatic_shot()
		#Check that more specialized logic is not needed

	def chival_cross(self):
		pass
		#Run recorded chival de fris cross operation

	def chival_cross_finished(self):
		pass
		#Called when recorded cross finished or aborted

	def straight_cross(self):
		pass
		#Call a straight macro
	def straight_cross_finished(self):
		pass
		#Called when straight macro aborted (won't finish on its own)

#op_finished methods should not actually disable the op_lock.
#That should be done by the final mechanism method to run for the operation.
#op_finished methods should be called either in abort portions of the mech controller
#or by the 


#op_finished mehtods should not actually disable the op_lcok
#the op_finished methods should really be op_abort methods that pass
#control to the necessary mechanism abort functions
#the proper mechanism finished functions (called in both the abort and normal sequences)
#should disable the op_lock.




