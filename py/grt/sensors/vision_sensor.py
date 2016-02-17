from grt.core import Sensor


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
        self.flywheel_at_speed = self.shooter.flywheel.flywheel_motor.getClosedLoopError() < \
                                 self.FLYWHEEL_SPEED_TOLERANCE
        self.rotation_ready = self.shooter.turntable.pid_controller.onTarget()
        self.vertical_ready = self.shooter.hood.hood_motor.getClosedLoopError() < \
                              self.HOOD_ANGLE_TOLERANCE
        self.rotational_error = self.shooter.robot_vision.rotational_error
        self.vertical_error = self.shooter.robot_vision.vertical_error
        self.target_view = self.shooter.robot_vision.target_view
