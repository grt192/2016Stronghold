__author__ = 'dhruv and alex m'

from grt.core import GRTMacro
import wpilib
import threading


# constants = Constants()


class PickupStraightMacro(GRTMacro):
    """
    Drive Macro; drives forwards a certain distance while
    maintaining orientation
    """


    DT_NO_TARGET_TURN_RATE = .2
    DT_KP = .03
    DT_KI = 0
    DT_KD = 0
    DT_ABS_TOL = 5
    DT_OUTPUT_RANGE = .25
    POWER = -.7

    def __init__(self, pickup_motor1, pickup_motor2, potentiometer1, potentiometer2, timeout=None):
        """
        Pass drivetrain, distance to travel (ft), and timeout (secs)
        """
        super().__init__(timeout)
        self.operation_manager = None
        self.pickup_motor1 = pickup_motor1
        self.pickup_motor2 = pickup_motor2
        self.potentiometer1 = potentiometer1
        self.potentiometer2 = potentiometer2
        self.enabled = False
        self.setpoint = None

        self.pid_controller = wpilib.PIDController(self.DT_KP, self.DT_KI,
                                                   self.DT_KD, self.get_input,
                                                   self.set_output)
        self.pid_controller.setAbsoluteTolerance(self.DT_ABS_TOL)
        self.pid_controller.reset()

        self.pid_controller.setInputRange(0.0, 360.0)
        self.pid_controller.setContinuous(True)

        self.pid_controller.setOutputRange(-.4, .4)
        #self.run_threaded()

    def macro_initialize(self):
        self.enable()
        threading.Timer(2.0, self.disable).start()

    def enable(self):
        self.setpoint = self.navx.fused_heading
        self.pid_controller.setSetpoint(self.setpoint)
        self.pid_controller.enable()
        self.enabled = True

    def disable(self):
        self.pid_controller.disable()
        self.setpoint = None
        self.enabled = False
        self.pickup_motor1.set(0)
        self.pickup_motor2.set(0)
        if not self.operation_manager == None:
            self.operation_manager.op_lock = False
        self.terminate()

    def set_output(self, output):
        if self.enabled:
            if not self.pid_controller.onTarget():
                self.potentiometer1.set(self.POWER + output)
                self.potentiometer1.set(self.POWER - output)
            else:
                self.dt.set_dt_output(self.POWER, self.POWER)

    def get_input(self):
        print("Input: ", (self.potentiometer1.angle - self.potentiometer2.angle))
        return self.potentiometer1.angle - self.potentiometer2.angle


