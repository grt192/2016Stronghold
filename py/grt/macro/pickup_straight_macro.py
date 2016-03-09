__author__ = 'dhruv and alex m'

from grt.core import GRTMacro
import wpilib
import threading
from grt.mechanism.pickup import Pickup

#constants = Constants()


class StraightMacro(GRTMacro):
    """
    Drive Macro; drives forwards a certain distance while
    maintaining orientation
    """

    # DT_NO_TARGET_TURN_RATE = .2
    PICKUP_KP = .03
    PICKUP_KI = 0
    PICKUP_KD = 0
    PICKUP_ABS_TOL = 5
    PICKUP_OUTPUT_RANGE = .25

    POWER_DEFAULT = -.7

    POWER = -.7

    JOYSTICK_POWER = .8

    def __init__(self, pickup: Pickup, timeout=None):
        """
        Pass drivetrain, distance to travel (ft), and timeout (secs)
        """
        super().__init__(timeout)
        self.set_forward()
        self.operation_manager = None

        self.enabled = False
        self.pickup = pickup

        self.setpoint = None
        self.driver_control = False

        self.pid_controller = wpilib.PIDController(self.PICKUP_KP, self.PICKUP_KI,
                                                   self.PICKUP_KD, self.get_input,
                                                   self.set_output)
        self.pid_controller.setAbsoluteTolerance(self.PICKUP_ABS_TOL)
        self.pid_controller.reset()

        self.pid_controller.setInputRange(0.0,  360.0)
        self.pid_controller.setContinuous(True)


        self.pid_controller.setOutputRange(-.4, .4)
        #self.run_threaded()

    def macro_initialize(self):
        self.enable()
        threading.Timer(2.0, self.disable).start()

    def macro_stop(self):
        self.disable()

    def enable_driver_control(self):
        self.driver_control = True

    def disable_driver_control(self):
        self.driver_control = False

    def set_forward(self):
        #Negative value is forward, positive value is reverse
        if self.POWER > 0:
            self.POWER *= -1

    def set_reverse(self):
        if self.POWER < 0:
            self.POWER *= -1


    def enable(self):
        self.setpoint = self.get_input()
        self.pid_controller.setSetpoint(self.setpoint)
        self.pid_controller.enable()
        self.enabled = True

    def disable(self):
        self.pid_controller.disable()
        self.setpoint = None
        self.enabled = False
        self.pickup.angle_change(0)
        if not self.operation_manager == None:
            self.operation_manager.op_lock = False
            #self.terminate()

    def set_output(self, output):
        """

        :param output: (-.5, .5)
        :return:
        """
        if self.enabled:
            if not self.pid_controller.onTarget():
                self.pickup.straight_macro_angle_change(self.POWER + output, self.POWER - output)

            else:
                self.pickup.straight_macro_angle_change(self.POWER, self.POWER)

            print("Setpoint: ", self.pid_controller.getSetpoint())
            print("Output: ", output)

    def get_input(self):
        input = self.pickup.achange_motor_1.getSensorPosition() - self.pickup.achange_motor_2.getSensorPosition()
        print("Input: ", input)
        return input