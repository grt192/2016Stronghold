from grt.core import GRTMacro
from grt.mechanism.operation_manager import OperationManager
from grt.mechanism.pickup import Pickup

__author__ = "dhruv"


class ChivalMacro(GRTMacro):
    """
    Run across chival de frise
    """

    def __init__(self, pickup: Pickup, straight_macro, operations_manager: OperationManager, timeout=3):
        super().__init__(timeout)
        self.operations_manager = operations_manager
        self.pickup = pickup
        self.straight_macro = straight_macro

    def initialize(self):
        self.operations_manager.ready_chival()
        self.pickup.go_to_frame_position()
        self._wait(.3)
        self.pickup.go_to_pickup_position()
        self._wait(.3)
        self.straight_macro.set_forward()
        self.straight_macro.enable()
        self._wait(2)
        self.straight_macro.disable()
        self.macro_stop()

    def macro_periodic(self):
        pass

    def macro_stop(self):
        self.operations_manager.chival_finish_cross()
