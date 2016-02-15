import wpilib
from grt.mechanism.flywheel import Flywheel, FlywheelSensor
from grt.mechanism.turntable import TurnTable, TurnTableSensor
from grt.mechanism.hood import Hood, HoodSensor
from grt.mechanism.rails import Rails
import threading
from wpilib import CANTalon




class Shooter:
    def __init__(self, robot_vision, flywheel_motor, turntable_motor, hood_motor, rails_actuator):
        self.operation_manager = None
        self.dt = None
        self.drivecontroller = None
        self.vision_enabled = False
        self.robot_vision = robot_vision
        self.flywheel_motor = flywheel_motor
        self.turntable_motor = turntable_motor
        self.hood_motor = hood_motor
        self.rails_actuator = rails_actuator
        self.target_locked_rotation = False
        self.target_locked_vertical = False
        self.geo_automatic = False
        self.vt_automatic = False
        self.shooter_timers_running = False
        self.is_shooting = False


        self.flywheel = Flywheel(self)
        self.turntable = TurnTable(self)
        self.hood = Hood(self)
        self.rails = Rails(self)

        self.flywheel_sensor = FlywheelSensor(self.flywheel)
        self.turntable_sensor = TurnTableSensor(self.turntable)
        self.hood_sensor = HoodSensor(self.hood)

        self.flywheel_sensor.add_listener(self._common_flywheel_listener)
        self.turntable_sensor.add_listener(self._vt_turntable_listener)
        self.hood_sensor.add_listener(self._vt_hood_listener)
        self.hood_sensor.add_listener(self._geo_hood_listener)




    def _vt_hood_listener(self, sensor, state_id, datum):
        if self.target_locked_rotation:
            if state_id == "vertical_ready":
                if datum:
                    self.target_locked_vertical = True
                else:
                    self.target_locked_vertical = False

    def _geo_hood_listener(self, sensor, state_id, datum):
        if self.geo_automatic:
            if state_id == "vertical_ready":
                if datum:
                    self.target_locked_vertical = True
                else:
                    self.target_locked_vertical = False

    def _common_flywheel_listener(self, sensor, state_id, datum):
        if self.target_locked_vertical:
            if state_id == "at_speed":
                if datum:
                    self.rails.rails_down()
                    self.is_shooting = True
                    # self.abort_timer.start() #Run the abort function after a specified timeout
                    threading.Timer(2.0, self.finish_automatic_shot).start()
    

    def _vt_turntable_listener(self, sensor, state_id, datum):
        if self.vt_automatic:
            if state_id == "rotation_ready":
                if datum:
                    self.target_locked_rotation = True
                    #self.turntable.PID_controller.disable()
                    #self.turntable_motor.set(0)
                    self.hood.go_to_target_angle()
                    self.flywheel.spin_to_target_speed()
                    if not self.drivecontroller == None:
                        self.drivecontroller.disable_manual_control()
                    if not self.dt == None:
                        self.dt.set_dt_output(0, 0)
                else:
                    self.target_locked_rotation = False






    def vt_automatic_shot(self):
        #self.dt.dt_left.changeControlMode(CANTalon.ControlMode.Position)
        #self.dt.dt_left.setP(.5)
        #self.dt.dt_left.set(0)
        #self.dt.dt_right.changeControlMode(CANTalon.ControlMode.Follower)
        #self.dt.dt_right.set(self.dt.dt_left.getDeviceID())
        #self.dt.dt_right.setP(.99)
        #self.dt.dt_right.reverseOutput(True)
        #self.dt.dt_right.set(0)
        #self.vision_enabled = True
        #threading.Timer(1.0, self.reverse_func).start()
        self.shooter_timers_running = True
        if self.rails.get_position() == "down":
            self.rails.rails_up()
            self.vt_reverse_func()
        else:
            self.vt_forward_func()

    def vt_forward_func(self):
        if self.shooter_timers_running:

            self.flywheel.spin_to_standby_speed()
            self.hood.go_to_standby_angle()
            self.turntable.disable_front_lock()
            self.turntable.turntable_motor.set(0)
            self.turntable.PID_controller.enable()
            self.vt_automatic = True

    def geo_automatic_shot():
        if self.rails.get_position() == "down":
            self.rails.rails_up()
            self.geo_reverse_func()
        else:
            self.geo_forward_func()


    def geo_forward_func(self):
        if self.shooter_timers_running:
            self.flywheel.spin_to_geo_speed()
            self.hood.go_to_geo_angle()
            self.geo_automatic = True

    def finish_automatic_shot(self):
        self.shooter_timers_running = False
        self.turntable.PID_controller.disable()
        self.turntable.enable_front_lock()
        #self.rails.rails_up()
        self.flywheel.spindown()
        #self.rails.rails_down()
        self.hood.go_to_frame_angle()
        #self.turntable.turntable_motor.set(0)
        if not self.drivecontroller == None:
            self.drivecontroller.enable_manual_control()
        self.target_locked_rotation = False
        self.target_locked_vertical = False
        self.geo_automatic = False
        self.vt_automatic = False
        self.is_shooting = False

        self.operation_manager.op_lock = False

    def abort_automatic_shot(self):   #Also aborts automatic pickup and automatic cross
        #self.spindown()
        if not self.is_shooting:
            self.shooter_timers_running = False
            self.turntable.PID_controller.disable()
            self.turntable.enable_front_lock()
            #self.rails.rails_up()
            self.flywheel.spindown()
            #self.rails.rails_down()
            self.hood.go_to_frame_angle()
            #self.turntable.turntable_motor.set(0)
            if not self.drivecontroller == None:
                self.drivecontroller.enable_manual_control()
            self.target_locked_rotation = False
            self.target_locked_vertical = False
            self.geo_automatic = False
            self.vt_automatic = False

            self.operation_manager.op_lock = False
         #Last item to be called in automatic shot operation
                                 #Flywheel reverse component of the operation will continue past the official operation end time.

    def vt_reverse_func(self):
        self.flywheel.spin_to_reverse_speed()
        threading.Timer(1.0, self.vt_forward_func).start()

    def geo_reverse_func(self):
        self.flywheel.spin_to_reverse_speed()
        threading.Timer(1.0, self.geo_forward_func).start()

    def final_stop_func(self):
        self.flywheel.spindown()
        #if not self.operation_manager == None:
        #    print("Op lock:", self.operation_manager.op_lock)
        #    self.operation_manager.op_lock = False

    def automatic_pickup(self):
        self.rails.rails_up()
        self.flywheel.spin_to_pickup_speed()

    

        

    
