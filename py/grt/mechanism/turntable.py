import wpilib
from grt.core import Sensor
import threading
from wpilib import CANTalon





class TurnTable:
    tt_override = False

    #ENC_MIN = -20000
    #ENC_MAX = 20000
    POT_MIN = 478
    POT_MAX = 505
    POT_CENTER = 495

    INITIAL_NO_TARGET_TURN_RATE = 0

    TURNTABLE_NO_TARGET_TURN_RATE = .1
    TURNTABLE_KP = .0018
    TURNTABLE_KI = 0
    TURNTABLE_KD = .008
    TURNTABLE_ABS_TOL = 10
    TURNTABLE_OUTPUT_RANGE = .4

    POT_TURN_KP = .01
    POT_TURN_KI = 0
    POT_TURN_KD = 0
    POT_TURN_OUTPUT_RANGE = .5

    def __init__(self, shooter):
        self.shooter = shooter
        self.turntable_motor = shooter.turntable_motor
        self.robot_vision = shooter.robot_vision
        self.dt = shooter.dt
        self.turntable_lock = threading.Lock()
        self.last_output = self.INITIAL_NO_TARGET_TURN_RATE
        self.prev_input = 0

        self.PID_controller = wpilib.PIDController(self.TURNTABLE_KP, self.TURNTABLE_KI, self.TURNTABLE_KD, self.get_input, self.set_output)
        self.PID_controller.setAbsoluteTolerance(self.TURNTABLE_ABS_TOL)
        self.PID_controller.reset()
        self.PID_controller.setOutputRange(-self.TURNTABLE_OUTPUT_RANGE, self.TURNTABLE_OUTPUT_RANGE)
        self.PID_controller.setInputRange(-300, 300)
        #Be sure to use tolerance buffer
        self.PID_controller.setSetpoint(35)

    def getRotationReady(self):
        #If an additional check is needed beyond PIDController.onTarget() for determining whether
        #the rotation is ready, use this function
        with self.turntable_lock:
            return self.PID_controller.onTarget()

    def get_input(self):
        if self.robot_vision.getTargetView():
            self.prev_input = self.robot_vision.getRotationalError()
            return self.prev_input
        else:
            return self.prev_input

   
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
        #print("Output: ", output, "    Position: ", self.turntable_motor.getPosition())
        if self.turntable_motor.getControlMode() == CANTalon.ControlMode.PercentVbus:
            if self.turntable_motor.getPosition() > self.POT_MIN and output > 0:
                self.turntable_motor.set(output)
            elif self.turntable_motor.getPosition() < self.POT_MAX and output < 0:
                self.turntable_motor.set(output)
            else:
                self.turntable_motor.set(0)
                print("Turntable exceeded max bounds")
        else:
            print("Turntable motor not in PercentVbus control mode!")
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

    
    def enable_front_lock(self):
        if not self.tt_override:
            self.turntable_motor.changeControlMode(CANTalon.ControlMode.Position)
            #self.turntable_motor.setFeedbackDevice() #Fix this to use a potentiometer!
            self.turntable_motor.setP(self.POT_TURN_KP)
            self.turntable_motor.set(0)

    def disable_front_lock(self):
        self.turntable_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.turntable_motor.set(0)



class TurnTableSensor(Sensor):
    def __init__(self, turntable):
        super().__init__()
        self.turntable = turntable
    def poll(self):
        self.rotation_ready = self.turntable.PID_controller.onTarget()
