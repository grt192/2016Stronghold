import wpilib
from grt.mechanism.flywheel import Flywheel, FlywheelSensor
from grt.mechanism.turntable import TurnTable, TurnTableSensor
from grt.mechanism.hood import Hood, HoodSensor
from grt.mechanism.rails import Rails
import threading




class Shooter:
    def __init__(self, robot_vision, flywheel_motor, turntable_motor, hood_motor, rails_actuator, dt):
        self.robot_vision = robot_vision
        self.flywheel_motor = flywheel_motor
        self.turntable_motor = turntable_motor
        self.hood_motor = hood_motor
        self.rails_actuator = rails_actuator
        self.dt = dt

        self.flywheel = Flywheel(self)
        self.turntable = TurnTable(self)
        self.hood = Hood(self)
        self.rails = Rails(self)

        self.flywheel_sensor = FlywheelSensor(self.flywheel)
        self.turntable_sensor = TurnTableSensor(self.turntable)
        self.hood_sensor = HoodSensor(self.hood)

        self.flywheel_sensor.add_listener(self._flywheel_listener)
        self.turntable_sensor.add_listener(self._turntable_listener)
        self.hood_sensor.add_listener(self._hood_listener)

        self.spindown_timer = threading.Timer(2.0, self.spindown)



    def spindown(self):
        self.flywheel.spindown()
        #self.raw_speed_spin(speed)
        #self.launcher.set(True)

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
            if datum:
                self.target_locked_rotation = True
                self.hood.go_to_target_angle()
                self.flywheel.spin_to_target_speed()
            else:
                self.target_locked_rotation = False


    def finish_automatic_shot(self):
        self.turntable.PID_controller.disable()
        self.turntable.turntable_sensor.on_target = False
        self.target_locked_vertical = False
        self.target_locked_rotation = False
        self.spindown_timer.start()

    def start_automatic_shot(self):
        self.flywheel.spin_to_standby_speed()
        self.turntable.PID_controller.enable()

    def abort_automatic_shot(self):
        self.spindown()
        self.turntable.PID_controller.disable()
        self.turntable.turntable_sensor.on_target = False
        self.target_locked_horizontal = False
        self.target_locked_vertical = False

    def start_geometric_shot(position=0):
        pass

        

    
