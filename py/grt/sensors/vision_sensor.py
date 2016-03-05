from grt.core import Sensor
from wpilib import CANTalon


class VisionSensor(Sensor):
    FLYWHEEL_SPEED_TOLERANCE = 50
    HOOD_ANGLE_TOLERANCE = 5

    def __init__(self, shooter=None):
        super().__init__()
        self.shooter = shooter
        self.rotational_error = self.vertical_error = self.target_view = None
        self.flywheel_at_speed = False
        self.rotation_ready = False
        self.vertical_ready = False

    def poll(self):
        self.flywheel_at_speed = self.shooter.flywheel.flywheel_motor.getClosedLoopError() < self.FLYWHEEL_SPEED_TOLERANCE
        self.rotation_ready = self.shooter.turntable.pid_controller.onTarget()
        if self.shooter.hood.hood_motor.getControlMode() == CANTalon.ControlMode.PercentVbus:
            self.vertical_ready = True
        else:
            self.vertical_ready = self.shooter.hood.hood_motor.getClosedLoopError() < self.HOOD_ANGLE_TOLERANCE
        # self.rotational_error = self.shooter.robot_vision.rotational_error
        # self.vertical_error = self.shooter.robot_vision.vertical_error
        # self.target_view = self.shooter.robot_vision.target_view

# class TurnTableSensor(Sensor):
#     def __init__(self, turntable):
#         super().__init__()
#         self.turntable = turntable
#     def poll(self):
#         self.rotation_ready = self.turntable.PID_controller.onTarget()

# class HoodSensor(Sensor):
#   ANGLE_TOLERANCE = 5
#
#   def __init__(self, hood):
#       super().__init__()
#       self.hood = hood
#
#   def poll(self):
#       if self.hood.hood_motor.getControlMode() == CANTalon.ControlMode.PercentVbus:
#           self.vertical_ready = True
#       else:
#           if self.hood.hood_motor.getClosedLoopError() < self.ANGLE_TOLERANCE:
#               self.vertical_ready = True
#           else:
#               self.vertical_ready = False
#
#
#


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

