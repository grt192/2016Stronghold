from wpilib import CANTalon
from grt.core import Sensor


class Flywheel:
    STANDBY_SPEED = -8400

    def __init__(self, robot_vision, flywheel_motor):
        self.flywheel_motor = flywheel_motor
        self.robot_vision = robot_vision
        self.current_speed = self.STANDBY_SPEED
        self.current_power = 0

    def spin_to_target_speed(self):
        if self.robot_vision.target_view:
            self.flywheel_motor.set((self.get_target_speed(self.robot_vision.vertical_error)))

    def get_target_speed(self, vertical_error):
        # TODO: Add conversion Constants
        return vertical_error

    def spin_to_standby_speed(self):
        self.flywheel_motor.set((self.STANDBY_SPEED))

    def spin_to_geo_speed(self):
        self.flywheel_motor.set(2600)

    def spin_to_pickup_speed(self):
        self.flywheel_motor.set(2000)

    def spin_to_reverse_speed(self):
        self.flywheel_motor.set(-1000)

    def spin_down(self):
        self.flywheel_motor.set(0)

    def increment_speed(self):
        self.current_speed -= 200
        self.flywheel_motor.set(self.current_speed)
        print("Current Set Speed: ", self.current_speed)

    def decrement_speed(self):
        self.current_speed -= 200
        self.flywheel_motor.set(self.currentspeed)
        print("Current Set Speed: ", self.current_speed)

    def increment_power(self):
        self.current_power += .1
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(self.current_power)

    def decrement_power(self):
        self.current_power -= .1
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(self.current_power)

    def spin_to_pickup_power(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(.5)


# class FlywheelSensor(Sensor):
#     SPEED_TOLERANCE = 50
#
#     def __init__(self, flywheel):
#         super().__init__()
#         self.flywheel = flywheel
#
#     def poll(self):
#         if self.flywheel.flywheel_motor.getClosedLoopError() < self.SPEED_TOLERANCE:
#             self.at_speed = True
#         else:
#             self.at_speed = False
