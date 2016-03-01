from wpilib import CANTalon
from grt.core import Sensor

class Flywheel:
    STANDBY_SPEED = 2600
    GEO_SPEED = 4000
    GEO_POWER = .8
    def __init__(self, robot_vision, flywheel_motor):
        self.flywheel_motor = flywheel_motor
        self.robot_vision = robot_vision
        self.currentspeed = self.STANDBY_SPEED
        self.current_power = 0

    def spin_to_target_speed(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
        if self.robot_vision.getTargetView():
            #self.rpm_speed_spin(self.robot_vision.getTargetSpeed())
            self.flywheel_motor.set(self.STANDBY_SPEED)

    def spin_to_standby_speed(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
        self.flywheel_motor.set(self.STANDBY_SPEED)

    def spin_to_geo_speed(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
        self.flywheel_motor.set(self.GEO_SPEED)

    def spin_to_geo_power(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(self.GEO_POWER)


    def spin_to_reverse_power(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(-.3)

    def spin_to_full_reverse_power(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(-1)

    def spin_to_full_power(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(1)

    def spindown(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(0)
    
    
    def speed_increment_function(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
        self.currentspeed=self.currentspeed+200
        self.flywheel_motor.set(self.currentspeed)

    def speed_decrement_function(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
        self.currentspeed=self.currentspeed-200
        self.flywheel_motor.set(self.currentspeed)

    def power_increment_function(self):
        self.current_power += .1
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(self.current_power)

    def power_decrement_function(self):
        self.current_power -= .1
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(self.current_power)

    def spin_to_pickup_power(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(.3)




        

    


class FlywheelSensor(Sensor):
    SPEED_TOLERANCE = 100

    def __init__(self, flywheel):
        super().__init__()
        self.flywheel = flywheel

    def poll(self):
        #print("Flywheel close loop error: ", self.flywheel.flywheel_motor.getClosedLoopError())
        if abs(self.flywheel.flywheel_motor.getClosedLoopError()) < self.SPEED_TOLERANCE:
            self.at_speed = True
        else:
            self.at_speed = False