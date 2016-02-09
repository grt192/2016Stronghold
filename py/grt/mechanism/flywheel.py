from wpilib import CANTalon
from grt.core import Sensor


class Flywheel:
    STANDBY_SPEED = -8400

    def __init__(self, robot_vision, flywheel_motor):
        self.flywheel_motor = flywheel_motor
        self.robot_vision = robot_vision
        self.currentspeed = self.STANDBY_SPEED

    def spin_to_target_speed(self):
        if self.robot_vision.target_view:
            vertical_error = self.robot_vision.vertical_error
            self.rpm_speed_spin(vertical_error)

    def spin_to_standby_speed(self):
        self.rpm_speed_spin(self.STANDBY_SPEED)

    def spin_down(self):
        self.rpm_speed_spin(0)

    def vbus_spin(self, power):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVBus)
        self.flywheel_motor.set(power)

    def voltage_spin(self, voltage):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.Voltage)
        self.flywheel_motor.set(voltage)

    def raw_speed_spin(self, speed):
        # self.flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
        # self.flywheel_motor.setP(1)
        self.flywheel_motor.set(speed)

    def rpm_speed_spin(self, speed):
        # ADD PROPER CONVERSION CONSTANTS
        self.raw_speed_spin(speed)

    def increment_speed(self):
        self.currentspeed -= 200
        self.rpm_speed_spin(self.currentspeed)
        print("Current Set Speed: ", self.currentspeed)

    def decrement_speed(self):
        self.currentspeed -= 200
        self.rpm_speed_spin(self.currentspeed)
        print("Current Set Speed: ", self.currentspeed)
