import wpilib
from grt.mechanism.flywheel import Flywheel, FlywheelSensor
from grt.mechanism.turntable import TurnTable, TurnTableSensor
from grt.mechanism.hood import Hood, HoodSensor
from grt.mechanism.rails import Rails
import threading, time
from wpilib import CANTalon




class Shooter:
    def __init__(self, robot_vision, flywheel_motor, turntable_motor, hood_motor, rails_actuator):

        self.GEO_SPINUP_TIME = 2.0

        """
        A reference will be passed to each of these controllers by the controller itself
        """
        self.operation_manager = None
        self.dt = None
        self.drivecontroller = None
        self.override_manager = None


        """
        These individual motors should be replaced with the complete mechanism classes found in the merged branch
        """
        self.robot_vision = robot_vision
        self.flywheel_motor = flywheel_motor
        self.turntable_motor = turntable_motor
        self.hood_motor = hood_motor
        self.rails_actuator = rails_actuator


        """
        These booleans control the automatic shot logic
        """
        self.target_locked_rotation = False
        self.target_locked_vertical = False
        self.geo_automatic = False
        self.vt_automatic = False
        self.shooter_timers_running = False
        self.is_shooting = False
        self.vision_enabled = False


        self.flywheel = Flywheel(self)
        self.turntable = TurnTable(self)
        self.hood = Hood(self)
        self.rails = Rails(self)

        self.flywheel_sensor = FlywheelSensor(self.flywheel)
        self.turntable_sensor = TurnTableSensor(self.turntable)
        self.hood_sensor = HoodSensor(self.hood)

    
    """
    Vision tracking logic loop, started by the vision tracking initialization code
    Checks that all parameters are good, then executes the shot
    """

    def vt_logic_loop(self):
        target_locked_rotation = target_locked_vertical = target_locked_speed = False
        while self.vt_automatic:
            time.sleep(.1)
            target_locked_rotation = self.check_rotation()
            target_locked_vertical = self.check_vertical()
            target_locked_speed = self.check_speed()
            
            if target_locked_rotation and target_locked_vertical and target_locked_speed:
                self.execute_shot()
    
    
    def check_rotation(self):
        target_locked_rotation = False
        if self.turntable_sensor.rotation_ready:
            target_locked_rotation = True
            self.flywheel.spin_to_target_speed()
            if self.drivecontroller:
                self.drivecontroller.disable_manual_control()
            if self.dt:
                self.dt.set_dt_output(0, 0)
        else:
            target_locked_rotation = False
            if self.drivecontroller:
                self.drivecontroller.enable_manual_control()
        return target_locked_rotation

    def check_vertical(self):
        return self.hood_sensor.vertical_ready

    def check_speed(self):
        return self.flywheel_sensor.at_speed

    

    def execute_shot(self):
        print("Executing shot")
        self.rails.rails_down()
        self.is_shooting = True
        threading.Timer(2.0, self.finish_automatic_shot).start()


    """
    Vision-tracking shot initialization
    If rails are up --> vt_automatic calls vt_forward directly
    If rails are down --> vt_automatic calls vt_reverse, then vt_delay, then vt_forward
    """

    def vt_automatic_shot(self):
        self.shooter_timers_running = True
        if self.rails.current_position == "down":
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

    """
    Geometric shot initialization
    If rails are up --> geo_automatic calls geo_forward directly
    If rails are down --> geo_automatic calls geo_reverse, then geo_delay, then geo_forward
    """

    def geo_automatic_shot(self):
        self.shooter_timers_running = True
        if self.rails.current_position == "down":
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
            self.flywheel.spin_to_geo_speed()
            self.hood.go_to_geo_angle()
            self.geo_automatic = True
            threading.Timer(self.GEO_SPINUP_TIME, self.execute_shot).start()




    """
    Shot completion and abort
    finish_automatic calls abort_core if the shot completed
    abort_automatic calls abort_core if the shot was aborted
    """

    def finish_automatic_shot(self):
        self.is_shooting = False
        self.abort_core()


    def abort_automatic_shot(self):   
        if not self.is_shooting:
            self.abort_core()

    def abort_core(self):
        self.geo_automatic = False
        self.vt_automatic = False
        self.shooter_timers_running = False
        self.turntable.PID_controller.disable()
        self.turntable.turntable_motor.set(0)
        self.turntable.enable_front_lock()
        self.flywheel.spindown()
        self.hood.go_to_frame_angle()
        if self.drivecontroller:
            self.drivecontroller.enable_manual_control()
        
        self.operation_manager.op_lock = False

    
         
    

    

        

    
