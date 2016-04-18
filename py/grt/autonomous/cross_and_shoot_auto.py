from grt.autonomous import MacroSequence
from grt.macro.shoot_macro import ShootMacro


class CrossAndShootAuto(MacroSequence):
    """
    Crosses a defense and shoots
    """

    def __init__(self, straight_macro, operations_manager, straight_macro_timeout=4, shoot_macro_timeout=6):

        shoot_macro = ShootMacro(operations_manager, timeout=shoot_macro_timeout)

        self.macros = [straight_macro, shoot_macro]
        super().__init__(macros=self.macros)