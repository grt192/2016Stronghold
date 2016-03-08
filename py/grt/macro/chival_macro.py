from grt.core import GRTMacro
from grt.mechanism.operation_manager import OperationManager
from grt.macro.straight_macro import StraightMacro

__author__ = "dhruv"


class ChivalMacro(GRTMacro):
    """
    Runs across the cival de frise
    """

    def __init__(self, pickup, straight_macro: StraightMacro, operations_manager: OperationManager, timeout=3):
        super().__init__(timeout)
        self.pickup = pickup
        self.straight_macro = straight_macro
        self.operations_manager = operations_manager

    def initialize(self):
        self.operations_manager.ready_chival()
        self.pickup.go_to_frame_position()
        self._wait(.3)

        self.straight_macro.set_forward()
        self.straight_macro.enable()
        self._wait(.4)
        self.straight_macro.disable()

        self.pickup.go_to_pickup_position()
        self._wait(.3)

        self.straight_macro.set_reverse()
        self.straight_macro.enable()
        self._wait(.2)
        self.straight_macro.disable()

        self.straight_macro.set_forward()
        self.straight_macro.enable()
        self._wait(4)
        self.straight_macro.disable()
        self.macro_stop()

    def macro_periodic(self):
        pass

    def macro_stop(self):
        self.operations_manager.shooter.abort_core()
