import wpilib
from grt.core import Sensor
import threading


ENC_MIN = 50
ENC_MAX = 51


class TurnTable:

    DT_NO_TARGET_TURN_RATE = .2
    INITIAL_NO_TARGET_TURN_RATE = .2

    def __init__(self, shooter):
        self.shooter = shooter
        self.robot_vision = shooter.robot_vision
        self.dt = shooter.dt
        self.turntable_lock = threading.Lock()
        self.last_output = self.INITIAL_NO_TARGET_TURN_RATE

        self.PID_controller = wpilib.PIDController(.0015, 0, 0, self.get_input, self.set_output)
        self.PID_controller.setAbsoluteTolerance(50)
        self.PID_controller.reset()
        self.PID_controller.setOutputRange(-.25, .25)
        #self.PID_controller.setInputRange(-300, 300)
        #Be sure to use tolerance buffer
        self.PID_controller.setSetpoint(0)

    def getRotationReady(self):
        with self.turntable_lock:
            return self.rotation_ready

    def get_input(self):
        #Make sure this checks getTargetView(), as well
        return self.robot_vision.getRotationalError()

    def no_view_timeout(self):
        pass
        
    def set_output(self, output):
        
        if self.robot_vision.getTargetView():
            if self.PID_controller.onTarget():
                #If the target is visible, and I'm on target, stop.
                output = 0
                self.dt_turn(output)
            else:
                #If the target is visible, and I'm not on target, keep going.
                self.dt_turn(output)
        else:
            if self.last_output > 0:
                #If the target is not visible, and I was moving forward, keep moving forward.
                output = self.DT_NO_TARGET_TURN_RATE
            elif self.last_output < 0:
                #If the target is not visible, and I was moving backward, keep moving backward.
                output = -self.DT_NO_TARGET_TURN_RATE
            elif self.last_output == 0:
                #If the target is not visible, but I was just on target, stay put.
                output = 0
            else:
                print("Last_output error!")
            self.dt_turn(output)
        self.last_output = output

    def turn(self, output):
        enc_pos = self.motor.getEncPosition()
        if output > 0:
            if enc_pos < ENC_MAX:
                #enc_pos < ENC_MAX:
                self.motor.set(output)
            else:
                self.motor.set(0)
        elif output < 0:
            if enc_pos > ENC_MIN:
                self.motor.set(output)
            else:
                self.motor.set(0)
        else:
            self.motor.set(0)

    def dt_turn(self, output):
        if self.dt:
            self.dt.set_dt_output(-output, -output)

    def turn_to(self, target):
        self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.motor.setP(1)
        self.motor.set(target) # TODO: WILL NOT CHANGE CONTROL MODE BACK



class TurnTableSensor(Sensor):
    def __init__(self, turntable):
        super().__init__()
        self.turntable = turntable
    def poll(self):
        self.rotation_ready = self.turntable.PID_controller.onTarget()
