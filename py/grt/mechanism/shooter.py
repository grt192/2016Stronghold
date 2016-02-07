import wpilib
from grt.mechanism.flywheel import Flywheel, FlywheelSensor
from grt.mechanism.turntable import TurnTable, TurnTableSensor
from grt.mechanism.hood import Hood, HoodSensor
from grt.core import Sensor
from grt.mechanism.rails import Rails
import threading
from wpilib import CANTalon


# THIS IS THE SAME AS THE VISION MECH CLASS
class ShooterNew:
    def __init__(self, robot_vision, vision_sensor, flywheel, turntable, hood, rails):
        self.robot_vision = robot_vision
        self.flywheel = flywheel
        self.turntable = turntable
        self.hood = hood
        self.rails = rails

    def spin_down(self):
        self.flywheel.spin_down()


class VisionSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.rotational_error = self.vertical_error = 0
        self.target_view = False

class Shooter:
    def __init__(self, robot_vision, flywheel, turntable, hood, rails):
        self.vision_enabled = False
        self.robot_vision = robot_vision
        self.flywheel = flywheel
        self.turntable = turntable
        self.hood = hood
        self.rails = rails
        self.target_locked_rotation = False
        self.target_locked_vertical = False

        self.flywheel_sensor = FlywheelSensor(self.flywheel)
        self.turntable_sensor = TurnTableSensor(self.turntable)
        self.hood_sensor = HoodSensor(self.hood)

        self.flywheel_sensor.add_listener(self._flywheel_listener)
        self.turntable_sensor.add_listener(self._turntable_listener)
        self.hood_sensor.add_listener(self._hood_listener)

        self.spindown_timer = threading.Timer(2.0, self.spindown)

    def spindown(self):
        self.flywheel.spin_down()
        # self.raw_speed_spin(speed)
        # self.launcher.set(True)

    def _hood_listener(self, sensor, state_id, datum):
        if self.target_locked_rotation:
            if state_id == "vertical_ready":
                if datum:
                    self.target_locked_vertical = True
                else:
                    self.target_locked_vertical = False

    def _flywheel_listener(self, sensor, state_id, datum):
        if self.target_locked_vertical:
            if state_id == "at_speed":
                if datum:
                    self.rails.rails_down()
                    self.finish_automatic_shot()



    def finish_automatic_shot(self):
        self.turntable.PID_controller.disable()
        self.turntable.turntable_sensor.on_target = False
        self.target_locked_vertical = False
        self.target_locked_rotation = False
        self.spindown_timer.start()

    def start_automatic_shot(self):
        # self.dt.dt_left.changeControlMode(CANTalon.ControlMode.Position)
        # self.dt.dt_left.setP(.5)
        # self.dt.dt_left.set(0)
        # self.dt.dt_right.changeControlMode(CANTalon.ControlMode.Follower)
        # self.dt.dt_right.set(self.dt.dt_left.getDeviceID())
        # self.dt.dt_right.setP(.99)
        # self.dt.dt_right.reverseOutput(True)
        # self.dt.dt_right.set(0)
        # self.vision_enabled = True

        # self.flywheel.spin_to_standby_speed()
        self.turntable.PID_controller.enable()

    def abort_automatic_shot(self):
        # self.spindown()
        self.turntable.PID_controller.disable()
        self.turntable_motor.set(0)
        self.turntable_sensor.rotation_ready = False
        self.target_locked_horizontal = False
        self.target_locked_vertical = False

    def start_geometric_shot(position=0):
        pass
