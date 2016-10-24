from grt.autonomous import MacroSequence


class NoLowAuto(MacroSequence):
    """
    Basic Autonomous. Runs the Straight Macro for 3 sec.
    """

    def __init__(self, no_low_macro):

        self.macros = [no_low_macro]
        super().__init__(macros=self.macros)
