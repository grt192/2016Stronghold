from grt.core import GRTMacro
from grt.mechanism.operation_manager import OperationManager

__author__ = "dhruv"


class ShootMacro(GRTMacro):
    """
    Runs a vision tracking shot
    """

    def __init__(self, operations_manager: OperationManager, timeout=3):
        super().__init__(timeout)
        self.operations_manager = operations_manager

    def initialize(self):
        self.operations_manager.vt_automatic_shot()

    def macro_periodic(self):
        if not self.operations_manager.shooter.shooter_timers_running and not self.operations_manager.shooter.is_shooting:
            self.terminate()

    def macro_stop(self):
        self.operations_manager.shooter.abort_core()
