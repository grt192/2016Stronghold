import wpilib
from grt.mechanism.flywheel import Flywheel, FlywheelSensor
from grt.mechanism.turntable import TurnTable, TurnTableSensor
from grt.mechanism.hood import Hood, HoodSensor
from grt.mechanism.rails import Rails
import threading, time
from wpilib import CANTalon


class Shooter:
    def __init__(self, robot_vision, flywheel, turntable, hood, rails):

        self.GEO_SPINUP_TIME = 2.0

        # A reference will be passed to each of these controllers by the controller itself
        self.operation_manager = None
        self.dt = None
        self.drivecontroller = None
        self.override_manager = None

        # These individual motors should be replaced with the complete mechanism classes found in the merged branch
        self.flywheel = flywheel
        self.rails = rails
        self.hood = hood
        self.turntable = turntable
        self.robot_vision = robot_vision

        # These booleans control the automatic shot logic
        self.target_locked_rotation = False
        self.target_locked_vertical = False
        self.geo_automatic = False
        self.vt_automatic = False
        self.shooter_timers_running = False
        self.is_shooting = False
        self.vision_enabled = False

        # Mechanism sensors
        self.flywheel_sensor = FlywheelSensor(self.flywheel)
        self.turntable_sensor = TurnTableSensor(self.turntable)
        self.hood_sensor = HoodSensor(self.hood)

    def vt_logic_loop(self):
        """
        Vision tracking logic loop, started by the vision tracking initialization code
        Checks that all parameters are good, then executes the shot
        """
        # target_locked_rotation = target_locked_vertical = target_locked_speed = False
        while self.vt_automatic:
            time.sleep(.1)
            # Check if turntable is locked on, spin up flywheel
            target_locked_rotation = self.check_rotation()

            # Check if hood is locked on
            target_locked_vertical = self.check_vertical()

            # Check if flywheel is at speed
            target_locked_speed = self.check_speed()

            if target_locked_rotation and target_locked_vertical and target_locked_speed:
                # If we are completely in position, execute the shot.
                self.execute_shot()

    def check_rotation(self):
        # target_locked_rotation = False
        if self.turntable_sensor.rotation_ready:
            # If the turntable is locked on, begin to spin up the flywheel
            target_locked_rotation = True
            self.flywheel.spin_to_target_speed()
            if self.drivecontroller:
                # Disable manual control for the time being.
                self.drivecontroller.disable_manual_control()
            if self.dt:
                # Disable the drivetrain so we stay put
                self.dt.set_dt_output(0, 0)
        else:
            # If the turntable is not locked on, return manual control to the drivers
            target_locked_rotation = False
            if self.drivecontroller:
                self.drivecontroller.enable_manual_control()

        return target_locked_rotation

    def check_vertical(self):
        # Check if hood is in position
        return self.hood_sensor.vertical_ready

    def check_speed(self):
        # Check if flywheel is at speed
        return self.flywheel_sensor.at_speed

    def execute_shot(self):
        print("Executing shot")
        self.rails.rails_down()
        self.is_shooting = True

        #
        threading.Timer(2.0, self.finish_automatic_shot).start()

    def vt_automatic_shot(self):
        """
        Vision-tracking shot initialization
        If rails are up --> vt_automatic calls vt_forward directly
        If rails are down --> vt_automatic calls vt_reverse, then vt_delay, then vt_forward
        """
        self.shooter_timers_running = True
        if not self.rails.is_up:
            self.rails.rails_up()
            self.vt_reverse_func()
        else:
            self.vt_forward_func()

    def vt_reverse_func(self):
        self.flywheel.spin_to_reverse_power()
        threading.Timer(1.0, self.vt_delay_func).start()

    def vt_delay_func(self):
        self.flywheel.spindown()
        threading.Timer(1.0, self.vt_forward_func).start()

    def vt_forward_func(self):
        if self.shooter_timers_running:
            self.flywheel.spin_to_standby_speed()
            self.hood.go_to_vt_angle()
            self.turntable.disable_front_lock()
            self.turntable.turntable_motor.set(0)
            self.turntable.PID_controller.enable()
            self.vt_automatic = True
            threading.Thread(target=self.vt_logic_loop).start()

    def geo_automatic_shot(self):
        """
        Geometric shot initialization
        If rails are up --> geo_automatic calls geo_forward directly
        If rails are down --> geo_automatic calls geo_reverse, then geo_delay, then geo_forward
        """
        self.shooter_timers_running = True
        if not self.rails.is_up:
            self.rails.rails_up()
            self.geo_reverse_func()
        else:
            self.geo_forward_func()

    def geo_reverse_func(self):
        self.flywheel.spin_to_reverse_power()
        threading.Timer(1.0, self.geo_delay_func).start()

    def geo_delay_func(self):
        self.flywheel.spindown()
        threading.Timer(1.0, self.geo_forward_func).start()

    def geo_forward_func(self):
        if self.shooter_timers_running:
            self.flywheel.spin_to_geo_power()
            self.hood.go_to_geo_angle()
            self.geo_automatic = True
            threading.Timer(self.GEO_SPINUP_TIME, self.execute_shot).start()

    def finish_automatic_shot(self):
        """
        Shot completion and abort
        finish_automatic calls abort_core if the shot completed
        abort_automatic calls abort_core if the shot was aborted
        """
        self.is_shooting = False
        self.abort_core()

    def abort_automatic_shot(self):
        if not self.is_shooting:
            self.abort_core()

    def abort_core(self):
        # Set booleans to false
        self.geo_automatic = False
        self.vt_automatic = False
        self.shooter_timers_running = False

        # Disable turntable PID control, and return it to it's locked forward state
        self.turntable.PID_controller.disable()
        self.turntable.enable_front_lock()

        # Spin down the flywheel, return hood to frame position for low-bar clearance
        self.flywheel.spindown()
        self.hood.go_to_frame_angle()

        # Re enable manual control
        if self.drivecontroller:
            self.drivecontroller.enable_manual_control()

        self.operation_manager.op_lock = False
