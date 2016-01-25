import wpilib
from grt.core import Sensor
import threading
import grt.mechanism.Constant


ENC_MIN = -20000
ENC_MAX = 20000


class TurnTable:

   
    DT_NO_TARGET_TURN_RATE = Constants.DT_NO_TARGET_TURN_RATE
    DT_KP = Constants.DT_KP
    DT_KI = Constant.DT_KI
    DT_KD = Constants.DT_KD
    DT_ABS_TOL = Constants.DT_ABS_TOL
    DT_OUTPUT_RANGE = Constants.DT_OUTPUT_RANGE

    INITIAL_NO_TARGET_TURN_RATE = 0

    TURNTABLE_NO_TARGET_TURN_RATE = .2
    TURNTABLE_KP = .002
    TURNTABLE_KI = 0
    TURNTABLE_KD = 0
    TURNTABLE_ABS_TOL = 10
    TURNTABLE_OUTPUT_RANGE = .4



    def __init__(self, shooter,Constants):
        self.shooter = shooter
        self.turntable_motor = shooter.turntable_motor
        self.robot_vision = shooter.robot_vision
        self.dt = shooter.dt
        self.turntable_lock = threading.Lock()
        self.last_output = self.INITIAL_NO_TARGET_TURN_RATE
        self.prev_input = 0
        self.Constants=Constants
        self.Constants.add_listener(self.Constants_listener)

        self.PID_controller = wpilib.PIDController(self.TURNTABLE_KP, self.TURNTABLE_KI, self.TURNTABLE_KD, self.get_input, self.set_output)
        self.PID_controller.setAbsoluteTolerance(self.TURNTABLE_ABS_TOL)
        self.PID_controller.reset()
        self.PID_controller.setOutputRange(-self.TURNTABLE_OUTPUT_RANGE, self.TURNTABLE_OUTPUT_RANGE)
        #self.PID_controller.setInputRange(-300, 300)
        #Be sure to use tolerance buffer
        self.PID_controller.setSetpoint(0)

    def getRotationReady(self):
        with self.turntable_lock:
            return self.rotation_ready

    def get_input(self):
        #Make sure this checks getTargetView(), as well
        if self.robot_vision.getTargetView():
            self.prev_input = self.robot_vision.getRotationalError()
            return self.prev_input
        else:
            return self.prev_input

    def no_view_timeout(self):
        pass
        
    def set_output(self, output):
        
        if self.robot_vision.getTargetView():
            if self.PID_controller.onTarget():
                #If the target is visible, and I'm on target, stop.
                output = 0
                #self.dt_turn(output)
                self.turn(output)
            else:
                #If the target is visible, and I'm not on target, keep going.
                #self.dt_turn(output)
                self.turn(output)
        else:
            if self.last_output > 0:
                #If the target is not visible, and I was moving forward, keep moving forward.
                #output = self.DT_NO_TARGET_TURN_RATE
                output = self.TURNTABLE_NO_TARGET_TURN_RATE
            elif self.last_output < 0:
                #If the target is not visible, and I was moving backward, keep moving backward.
                #output = -self.DT_NO_TARGET_TURN_RATE
                output = -self.TURNTABLE_NO_TARGET_TURN_RATE
            elif self.last_output == 0:
                #If the target is not visible, but I was just on target, stay put.
                output = 0
            else:
                print("Last_output error!")
            #self.dt_turn(output)
            self.turn(output)
        self.last_output = output

    def turn(self, output):
        #enc_pos = self.turntable_motor.getEncPosition()
        #if output > 0:
        #    if enc_pos < ENC_MAX:
                #enc_pos < ENC_MAX:
        self.turntable_motor.set(output)
            #else:
             #   self.turntable_motor.set(0)
        #elif output < 0:
         #   if enc_pos > ENC_MIN:
          #      self.turntable_motor.set(output)
           # else:
          #      self.turntable_motor.set(0)
        #else:
         #   self.turntable_motor.set(0)

    def dt_turn(self, output):
        if self.dt:
            self.dt.set_dt_output(-output, -output)

    def turn_to(self, target):
        self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.motor.setP(1)
        self.motor.set(target) # TODO: WILL NOT CHANGE CONTROL MODE BACK

    def Constants_listener(self, sensor, state_id, datum)
        if state_id in self.__dict__.keys():
            if datum:
                self.__dict__[state_id]=datum 






class TurnTableSensor(Sensor):
    def __init__(self, turntable):
        super().__init__()
        self.turntable = turntable
    def poll(self):
        self.rotation_ready = self.turntable.PID_controller.onTarget()
