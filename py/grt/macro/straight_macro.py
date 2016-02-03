__author__ = 'dhruv and alex m'

from grt.core import GRTMacro
import wpilib
import threading

#constants = Constants()


class StraightMacro(GRTMacro):
    """
    Drive Macro; drives forwards a certain distance while
    maintaining orientation
    """

    DT_NO_TARGET_TURN_RATE = .2
    DT_KP = .0015
    DT_KI = 0
    DT_KD = 0
    DT_ABS_TOL = 3
    DT_OUTPUT_RANGE = .25

    def __init__(self, dt, navx, timeout=None):
        """
        Pass drivetrain, distance to travel (ft), and timeout (secs)
        """
        super().__init__(timeout)
        self.dt = dt
        self.enabled = False
        self.navx = navx

        self.setpoint = None



        self.pid_controller = wpilib.PIDController(self.DT_KP, self.DT_KI,
                                                   self.DT_KD, self.get_input,
                                                   self.set_output)
        self.pid_controller.setAbsoluteTolerance(self.DT_ABS_TOL)
        self.pid_controller.reset()

        self.pid_controller.setInputRange(-180.0,  180.0)
        self.pid_controller.setContinuous(True)


        self.pid_controller.setOutputRange(-.5, .5)
        self.run_threaded()


    def enable(self):
        self.setpoint = self.navx.fused_heading
        self.pid_controller.setSetpoint(self.setpoint)
        self.pid_controller.enable()
        self.enabled = True

    def disable(self):
        self.pid_controller.disable()
        self.setpoint = None
        self.enabled = False

    def set_output(self, output):
        """

        :param output: (-.5, .5)
        :return:
        """
        if self.enabled:
            self.dt.set_dt_output(.4 + output, -(.4 +output))

    def get_input(self):
        return self.navx.fused_heading