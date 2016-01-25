import wpilib
from grt.core import Sensor
import threading

ENC_MIN = -20000
ENC_MAX = 20000


class TurnTable:
    DT_NO_TARGET_TURN_RATE = .2
    DT_KP = .0015
    DT_KI = 0
    DT_KD = 0
    DT_ABS_TOL = 50
    DT_OUTPUT_RANGE = .25

    INITIAL_NO_TARGET_TURN_RATE = 0

    TURNTABLE_NO_TARGET_TURN_RATE = .2
    TURNTABLE_KP = .0015
    TURNTABLE_KI = 0
    TURNTABLE_KD = 0
    TURNTABLE_ABS_TOL = 20
    TURNTABLE_OUTPUT_RANGE = .4

    def __init__(self, robot_vision, turntable_motor, dt):
        self.turntable_motor = turntable_motor
        self.robot_vision = robot_vision
        self.dt = dt

        self.last_output = self.INITIAL_NO_TARGET_TURN_RATE
        self.last_input = 0

        self.PID_controller = wpilib.PIDController(self.TURNTABLE_KP, self.TURNTABLE_KI, self.TURNTABLE_KD,
                                                   self.get_input, self.set_output)
        self.PID_controller.setAbsoluteTolerance(self.TURNTABLE_ABS_TOL)

        # TODO Workaround for wpilib bug as of 1/23/2016
        self.PID_controller.reset()

        # Be sure to use tolerance buffer
        self.PID_controller.setOutputRange(-self.TURNTABLE_OUTPUT_RANGE, self.TURNTABLE_OUTPUT_RANGE)
        self.PID_controller.setSetpoint(0)



    def get_input(self):
        # Make sure this checks getTargetView(), as well
        if self.robot_vision.target_view:
            self.last_input = self.robot_vision.rotational_error
            return self.last_input
        else:
            return self.last_input

    def no_view_timeout(self):  # TODO: Implement
        pass

    def set_output(self, output):

        if self.robot_vision.target_view():
            if self.PID_controller.onTarget():
                # If the target is visible, and I'm on target, stop.
                output = 0
                # self.dt_turn(output)
                self.turn(output)

            else:
                # If the target is visible, and I'm not on target, keep going.
                # self.dt_turn(output)
                self.turn(output)
        else:
            if self.last_output > 0:
                # If the target is not visible, and I was moving forward, keep moving forward.
                output = self.TURNTABLE_NO_TARGET_TURN_RATE

            elif self.last_output < 0:
                # If the target is not visible, and I was moving backward, keep moving backward.
                output = -self.TURNTABLE_NO_TARGET_TURN_RATE

            elif self.last_output == 0:
                # If the target is not visible, but I was just on target, stay put.
                output = 0

            else:
                print("Last_output error!")

            self.turn(output)
        self.last_output = output

    def turn(self, output):
        self.turntable_motor.set(output)

    def dt_turn(self, output):
        if self.dt:
            self.dt.set_dt_output(-output, -output)

    def turn_to(self, target):
        self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.motor.setP(1)
        self.motor.set(target)  # TODO: WILL NOT CHANGE CONTROL MODE BACK


class TurnTableSensor(Sensor):
    def __init__(self, turntable):
        super().__init__()
        self.turntable = turntable

    def poll(self):
        self.rotation_ready = self.turntable.PID_controller.onTarget()
