from wpilib import CANTalon
from grt.core import Sensor

class Flywheel:
    STANDBY_SPEED = 500
    def __init__(self, shooter):
        self.shooter = shooter
        self.flywheel_motor = shooter.flywheel_motor
        self.robot_vision = shooter.robot_vision

    def spin_to_target_speed(self):
        self.rpm_speed_spin(self.robot_vision.target_speed)
    def spin_to_standby_speed(self):
        self.rpm_speed_spin(self.STANDBY_SPEED)
    def spindown(self):
        self.rpm_speed_spin(0)

    def vbus_spin(self, power):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVBus)
        self.flywheel_motor.set(power)
    def voltage_spin(self, voltage):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.Voltage)
        self.flywheel_motor.set(voltage)
    def raw_speed_spin(self, speed):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
        self.flywheel_motor.setP(1)
        self.flywheel_motor.set(speed)
    def rpm_speed_spin(self, speed):
        #ADD PROPER CONVERSION CONSTANTS
        self.raw_speed_spin(speed)
    


class FlywheelSensor(Sensor):
    SPEED_TOLERANCE = 50

    def __init__(self, flywheel):
        super().__init__()
        self.flywheel = flywheel

    def poll(self):
        if self.flywheel.flywheel_motor.getClosedLoopError() < self.SPEED_TOLERANCE:
            self.at_speed = True
        else:
            self.at_speed = False