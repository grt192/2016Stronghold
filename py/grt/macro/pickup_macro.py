from grt.core import GRTMacro
from grt.mechanism.operation_manager import OperationManager
from grt.macro.straight_macro import StraightMacro

__author__ = "dhruv"


class PickupMacro(GRTMacro):
    """
    Runs across the chival de frise
    """

    def __init__(self, operations_manager, ball_switch, timeout=5):
        super().__init__(timeout)
        self.operations_manager = operations_manager
        self.ball_switch = ball_switch

    def initialize(self):
        self.operations_manager.manual_pickup()

    def macro_periodic(self):
        if self.ball_switch.s.get():
            self.macro_stop()

    def macro_stop(self):
        self.operations_manager.manual_pickup_abort()
        self.operations_manager.shooter.abort_core()
        self.terminate()
