from grt.autonomous import MacroSequence
from grt.macro.straight_macro import StraightMacro


class BasicAuto(MacroSequence):
    """
    Basic Autonomous. Runs the Straight Macro for 3 sec.
    """

    def __init__(self, straight_macro, timeout=4):

        self.macros = [straight_macro]
        super().__init__(macros=self.macros)
