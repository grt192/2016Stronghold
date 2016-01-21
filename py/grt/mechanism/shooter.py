import wpilib
from grt.mechanism.flywheel import Flywheel, FlywheelSensor
from grt.mechanism.turntable import TurnTable, TurnTableSensor
from grt.mechanism.hood import Hood, HoodSensor
from grt.mechanism.rails import Rails
import threading
from wpilib import CANTalon




class Shooter:
    def __init__(self, robot_vision, flywheel_motor, turntable_motor, hood_motor, rails_actuator, dt):
        self.vision_enabled = False
        self.robot_vision = robot_vision
        self.flywheel_motor = flywheel_motor
        self.turntable_motor = turntable_motor
        self.hood_motor = hood_motor
        self.rails_actuator = rails_actuator
        self.dt = dt
        self.target_locked_rotation = False
        self.target_locked_vertical = False

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
                self.target_locked_rotation = False
                #self.turntable.PID_controller.disable()
                self.hood.go_to_target_angle()
                #self.flywheel.spin_to_target_speed()
            else:
                self.target_locked_rotation = False

    def _vision_listener(self, sensor, state_id, datum):
        pass
        """
        if self.vision_enabled:
            if state_id == "rotational_error":
                if datum:
                    self.dt.dt_left.changeControlMode(CANTalon.ControlMode.Position)
                    self.dt.dt_left.setSensorPosition(datum)
                    self.dt.dt_right.setSensorPosition(datum)
                else:
                    self.dt.dt_left.changeControlMode(CANTalon.ControlMode.PercentVbus)
                    self.dt.dt_left.set(.5)
        """


    def finish_automatic_shot(self):
        self.turntable.PID_controller.disable()
        self.turntable.turntable_sensor.on_target = False
        self.target_locked_vertical = False
        self.target_locked_rotation = False
        self.spindown_timer.start()

    def start_automatic_shot(self):
        #self.dt.dt_left.changeControlMode(CANTalon.ControlMode.Position)
        #self.dt.dt_left.setP(.5)
        #self.dt.dt_left.set(0)
        #self.dt.dt_right.changeControlMode(CANTalon.ControlMode.Follower)
        #self.dt.dt_right.set(self.dt.dt_left.getDeviceID())
        #self.dt.dt_right.setP(.99)
        #self.dt.dt_right.reverseOutput(True)
        #self.dt.dt_right.set(0)
        #self.vision_enabled = True

        #self.flywheel.spin_to_standby_speed()
        self.turntable.PID_controller.enable()

    def abort_automatic_shot(self):
        self.spindown()
        self.turntable.PID_controller.disable()
        self.turntable_sensor.rotation_ready = False
        self.target_locked_horizontal = False
        self.target_locked_vertical = False

    def start_geometric_shot(position=0):
        pass

        

    
