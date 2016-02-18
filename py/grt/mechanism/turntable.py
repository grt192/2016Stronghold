import wpilib
from wpilib import CANTalon
from grt.core import Sensor


class TurnTable:
    tt_override = False

    POT_MIN = -20000
    POT_MAX = 20000

    POT_TURN_KP = .01
    POT_TURN_KI = 0
    POT_TURN_KD = 0
    POT_TURN_OUTPUT_RANGE = .5

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

    def __init__(self, robot_vision, turntable_motor: CANTalon, dt):
        self.turntable_motor = turntable_motor
        self.robot_vision = robot_vision
        self.dt = dt
        self.dt_assistance = False

        self.last_output = self.INITIAL_NO_TARGET_TURN_RATE
        self.last_input = 0

        self.pid_controller = wpilib.PIDController(self.TURNTABLE_KP, self.TURNTABLE_KI, self.TURNTABLE_KD,
                                                   self.pid_input, self.pid_output)

        self.pid_controller.setAbsoluteTolerance(self.TURNTABLE_ABS_TOL)

        # TODO: Workaround for wpilib/robotpy bug as of 1/23/2016
        self.pid_controller.reset()

        # Be sure to use tolerance buffer
        self.pid_controller.setOutputRange(-self.TURNTABLE_OUTPUT_RANGE, self.TURNTABLE_OUTPUT_RANGE)
        self.pid_controller.setSetpoint(0)

    def pid_input(self):
        # Make sure this checks target_view, as well
        if self.robot_vision.target_view:
            self.last_input = self.robot_vision.rotational_error
            return self.last_input
        else:
            return self.last_input

    def no_view_timeout(self):  # TODO: Implement
        pass

    def set_output(self, output):
        self.pot_pos = self.turntable_motor.getPosition()
        if self.robot_vision.target_view:
            if self.pid_controller.onTarget():
                # If the target is visible, and I'm on target, stop.
                output = 0
                # self.dt_turn(output)
                self.turn(output)
            else:
                if self.dt_assistance:
                    if self.POT_MAX > self.pot_pos > self.POT_MIN:
                        # If the target is visible, I'm in the pot turn tolerence, and I'm not on target, keep going.
                        self.turn(output)
                    else:
                        # If the target is visible, and I'm outside of the pot turn tolerence, and I'm not on target
                        # stop the turntable and turn the dt
                        output = self.DT_NO_TARGET_TURN_RATE
                        self.turn(0)
                        self.dt_turn(output)
                else:
                    # self.dt_turn(output)
                    self.turn(output)
        else:
            if self.last_output > 0:
                # If the target is not visible, and I was moving forward, keep moving forward.
                # output = self.TURNTABLE_NO_TARGET_TURN_RATE
                output = self.DT_NO_TARGET_TURN_RATE
            elif self.last_output < 0:
                # If the target is not visible, and I was moving backward, keep moving backward.
                # output = -self.TURNTABLE_NO_TARGET_TURN_RATE
                output = -self.DT_NO_TARGET_TURN_RATE
            elif self.last_output == 0:
                # If the target is not visible, but I was just on target, stay put.
                output = 0
            else:
                print("Last_output error!")

            # self.turn(output)
            self.dt_turn(output)

        self.last_output = output

    def turn(self, output):
        self.turntable_motor.set(output)

    def dt_turn(self, output):
        if self.dt:
            self.dt.set_dt_output(-output, -output)

    def turn_to(self, target):
        self.turntable_motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.turntable_motor.setP(1)
        self.turntable_motor.set(target) # TODO: WILL NOT CHANGE CONTROL MODE BACK

    def enable_front_lock(self):
        if not self.tt_override:
            self.turntable_motor.changeControlMode(CANTalon.ControlMode.Position)
            #self.turntable_motor.setFeedbackDevice() #Fix this to use a potentiometer!
            self.turntable_motor.setP(self.POT_TURN_KP)
            self.turntable_motor.set(0)

    def disable_front_lock(self):
        self.turntable_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.turntable_motor.set(0)



# class TurnTableSensor(Sensor):
#     def __init__(self, turntable):
#         super().__init__()
#         self.turntable = turntable
#     def poll(self):
#         self.rotation_ready = self.turntable.PID_controller.onTarget()
