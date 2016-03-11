from grt.core import GRTMacro
from grt.mechanism.pickup import Pickup
import threading
from grt.macro.straight_macro import StraightMacro
import time

__author__ = "dhruv"


class PortcullisMacro(GRTMacro):
    """
    Automatically runs across portcullis
    """

    def __init__(self, pickup: Pickup, straight_macro: StraightMacro, timeout=5):
        super().__init__(timeout)
        self.pickup = pickup
        self.straight_macro = straight_macro
        self.abort = False
        self.running_angle_change = False


    def _angle_change_with_abort(self):
        self.running_angle_change = True
        self.pickup.angle_change(.6)

    def abort(self):
        self.abort = True

    def enable(self):
        print("Running portcullis_macro")
        self.abort = False
        self.pickup.go_to_pickup_position()
        self._angle_change_with_abort()
        angle_change_timer = threading.Timer(2, self.disable)
        print("running achange timer")
        angle_change_timer.start()
        print("finished achange timer")


        while self.running_angle_change:
            pass

        self.straight_macro.set_forward()
        self.straight_macro.enable()
        straight_macro_timer = threading.Timer(2, self.straight_macro.disable)
        straight_macro_timer.start()

        # self.disable()

    def macro_periodic(self):
        pass

    def disable(self):
        self.running_angle_change = False
        print("disabling portcullis_macro")
        self.abort = True
        self.pickup.angle_change(0)