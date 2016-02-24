from wpilib import CANTalon
from grt.core import Sensor


class Hood:
    HOOD_MIN = 155
    HOOD_MAX = 385
    def __init__(self, shooter):
        self.shooter = shooter
        self.hood_motor = shooter.hood_motor
        self.robot_vision = shooter.robot_vision

    def go_to_target_angle(self):
        if self.robot_vision.getTargetView():
            self.auto_set(self.robot_vision.getTargetAngle())

    def go_to_standby_angle(self):
        self.auto_set(1000)

    def go_to_frame_angle(self):
        self.auto_set(0)

    def auto_set(self, angle):
        if self.hood_motor.getControlMode() == CANTalon.ControlMode.PercentVbus:
            return
        else:
            self.hood_motor.set(angle)

    def rotate(self, power):
        print("Motor power: ", power, "    Sensor Position: ", self.hood_motor.getPosition())
        if self.hood_motor.getControlMode() == CANTalon.ControlMode.PercentVbus:
            if power > 0 and self.hood_motor.getPosition() < self.HOOD_MAX:
                self.hood_motor.set(power)
            elif power < 0 and self.hood_motor.getPosition() > self.HOOD_MIN:
                self.hood_motor.set(power)
            else:
                print("Hood reached maximum angle")
                self.hood_motor.set(0)
        else:
            print("Hood motor not in PercentVbus control mode!")

    def enable_automatic_control(self):
        self.hood_motor.changeControlMode(CANTalon.ControlMode.Position)
        self.hood_motor.setP(.01)

    def disable_automatic_control(self):
        self.hood_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)


class HoodSensor(Sensor):
    ANGLE_TOLERANCE = 5

    def __init__(self, hood):
        super().__init__()
        self.hood = hood

    def poll(self):
        if self.hood.hood_motor.getControlMode() == CANTalon.ControlMode.PercentVbus:
            self.vertical_ready = True
        else:
            if self.hood.hood_motor.getClosedLoopError() < self.ANGLE_TOLERANCE:
                self.vertical_ready = True
            else:
                self.vertical_ready = False



