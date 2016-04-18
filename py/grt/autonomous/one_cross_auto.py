
from . import MacroSequence

class OneCrossAuto(MacroSequence):

	def __init__(self, straight_macro):
		self.straight_macro = straight_macro
		self.straight_macro.set_forward()
		self.macros = [self.straight_macro]
		super().__init__(macros=self.macros)