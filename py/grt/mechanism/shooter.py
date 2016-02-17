import threading


# THIS IS THE SAME AS THE 'VISION_MECH' CLASS

class Shooter:
    def __init__(self, robot_vision, vision_sensor, flywheel, turntable, hood, rails, vision_enabled=False):
        self.robot_vision = robot_vision
        self.flywheel = flywheel
        self.turntable = turntable
        self.hood = hood
        self.rails = rails

        self.vision_sensor = vision_sensor
        if not self.vision_sensor.shooter:
            self.vision_sensor.shooter = self

        self.target_locked_rotation = False
        self.target_locked_vertical = False

        self.vision_sensor.add_listener(self._flywheel_listener)
        self.vision_sensor.add_listener(self._hood_listener)
        self.vision_sensor.add_listener(self._turntable_listener)

        self.spindown_timer = threading.Timer(2.0, self.spin_down)
        self.vision_enabled = vision_enabled

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

    def _turntable_listener(self, sensor, state_id, datum):
        if state_id == "rotation_ready":
            print("ROTATION READY LISTENER")
            if datum:
                print("ROTATION IS READY")
                self.target_locked_rotation = True
                print("TARGET LOCKED ROTATION TRUE")
                # self.turntable.PID_controller.disable()
                # self.turntable_motor.set(0)
                # self.hood.go_to_target_angle()
                # self.flywheel.spin_to_target_speed()
            else:
                self.target_locked_rotation = False

    def turn(self, power):
        self.turntable.turn(power)

    def spin_flywheel(self, power):
        self.flywheel.vbus_spin(power)

    def shooter_down(self):
        self.rails.rails_down()

    def shooter_up(self):
        self.rails.rails_up()

    def spin_down(self):
            self.flywheel.spin_down()

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
        self.turntable.pid_controller.enable()

    def abort_automatic_shot(self):
        # self.spindown()
        self.turntable.pid_controller.disable()
        self.turntable.turntable_motor.set(0)
        self.vision_sensor.rotation_ready = False
        self.target_locked_rotation = False
        self.target_locked_vertical = False

    def finish_automatic_shot(self):
        self.turntable.pid_controller.disable()
        self.target_locked_vertical = False
        self.target_locked_rotation = False
        self.spindown_timer.start()
