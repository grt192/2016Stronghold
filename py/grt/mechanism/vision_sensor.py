from grt.core import Sensor


class VisionSensor(Sensor):
    HOOD_ANGLE_TOLERANCE = 5
    FLYWHEEL_SPEED_TOLERANCE = 50

    def __init__(self, shooter):
        super().__init__()
        # Mechanisms
        self.shooter = shooter

        # Vision Tracking Values--Polling occurs in robot_vision.py, no need to do it here.
        self.rotational_error = self.vertical_error = 0
        self.target_view = False

        # Turntable
        self.turntable_rotation_ready = False

        # Hood
        self.vertical_error = 0

        # Flywheel
        self.flywheel_at_speed = False

    def poll(self):
        # Polling / updating of rotational_error, vertical_error, target_view occurs in robot_vision;
        # no need to poll these attributes.

        self.turntable_rotation_ready = self.shooter.turntable.pid_controller.onTarget()
        self.vertical_error = self.shooter.hood.hood_motor.getClosedLoopError() < self.HOOD_ANGLE_TOLERANCE

        # Flywheel Speed
        if self.shooter.flywheel.flywheel_motor.getClosedLoopError() < self.FLYWHEEL_SPEED_TOLERANCE:
            self.flywheel_at_speed = True
        else:
            self.flywheel_at_speed = False