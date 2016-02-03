from grt.core import GRTMacro
import wpilib
import threading


class NewTurnMacro(GRTMacro):
    def __init__(self, target_angle, navx, dt):
        self.target_angle = target_angle
        self.navx = navx
        self.dt = dt

        self.kP = 0.03
        self.kI = 0.00
        self.kD = 0.00
        self.kF = 0.00
        self.kToleranceDegrees = 2.0

        self.turn_controller = wpilib.PIDController(self.kP, self.kI, self.kD, self.kF, self.ahrs, output=self.PIDSetDT)
        self.turn_controller.setInputRange(-180.0, 180.0)
        self.turn_controller.setOutputRange(-1.0, 1.0)
        self.turn_controller.setAbsoluteTolerance(self.kToleranceDegrees)
        self.turn_controller.setContinuous(True)

        self.turn_controller.setSetpoint(self.target_angle)

    def macro_initialize(self):
        self.turn_controller.enable()

    def macro_stop(self):
        self.turn_controller.disable()

    def PIDSetDT(self, output):
        self.dt.set_dt_output(output, -output)
