from wpilib import CANTalon
from grt.core import Sensor

class Flywheel:
    STANDBY_SPEED = 2550
    GEO_POWER = .8
    GEO_SPEED = 2600
    def __init__(self, shooter):
        self.shooter = shooter
        self.flywheel_motor = shooter.flywheel_motor
        self.robot_vision = shooter.robot_vision

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
        self.flywheel_motor.set(-.4)

    def spin_to_full_reverse_power(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(-1)

    def spin_to_full_power(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(1)

    def spindown(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(0)
    
    
    def increment_vt_speed(self):
        self.STANDBY_SPEED += 200
        print("Current vt speed: ", self.STANDBY_SPEED)
        #self.flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
        #self.currentspeed=self.currentspeed+200
        #self.flywheel_motor.set(self.currentspeed)

    def decrement_vt_speed(self):
        self.STANDBY_SPEED -= 200
        print("Current vt speed: ", self.STANDBY_SPEED)
        #self.flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
        #self.currentspeed=self.currentspeed-200
        #self.flywheel_motor.set(self.currentspeed)

    def increment_geo_power(self):
        self.GEO_POWER += .1
        print("Current geo power: ", self.GEO_POWER)
        #self.current_power += .1
        #self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        #self.flywheel_motor.set(self.current_power)

    def decrement_geo_power(self):
        self.GEO_POWER -= .1
        print("Current geo power: ", self.GEO_POWER)

    def increment_geo_speed(self):
        self.GEO_SPEED += 200
        print("Current geo speed: ", self.GEO_SPEED)

    def decrement_geo_speed(self):
        self.GEO_SPEED -= 200
        print("Current geo speed: ", self.GEO_SPEED)

        #self.current_power -= .1
        #self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        #self.flywheel_motor.set(self.current_power)

    def spin_to_pickup_power(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(.19)




        

    


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