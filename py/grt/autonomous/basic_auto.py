from grt.autonomous import MacroSequence
from grt.macro.straight_macro import StraightMacro


class BasicAuto(MacroSequence):
    """
    Basic Autonomous. Runs the Straight Macro for 3 sec.
    """

    def __init__(self, dt, navx, timeout=4):
        straight_macro = StraightMacro(dt, navx, timeout)
        straight_macro.set_forward()

        self.macros = [straight_macro]
        super().__init__(macros=self.macros)
