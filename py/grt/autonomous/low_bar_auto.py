from grt.autonomous import MacroSequence


class LowBarAuto(MacroSequence):
    """
    Basic Autonomous. Runs the Straight Macro for 3 sec.
    """

    def __init__(self, low_bar_macro):

        self.macros = [low_bar_macro]
        super().__init__(macros=self.macros)
