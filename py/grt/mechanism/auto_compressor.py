
class AutoCompressor:

	def __init__(self, compressor):
		self.compressor = compressor
		self.override_manager = None

	def enable_control(self):
		if self.override_manager:
			if not self.override_manager.power_conserve:
				self.compressor.start()

	def disable_control(self):
		self.compressor.stop()