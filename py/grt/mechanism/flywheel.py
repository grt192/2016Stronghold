from wpilib import CANTalon
from grt.core import Sensor

class Flywheel:
    STANDBY_SPEED = -8400
    def __init__(self, shooter):
        self.shooter = shooter
        self.flywheel_motor = shooter.flywheel_motor
        self.robot_vision = shooter.robot_vision
        self.currentspeed = self.STANDBY_SPEED

    def spin_to_target_speed(self):
        if self.robot_vision.getTargetView():
            #self.rpm_speed_spin(self.robot_vision.getTargetSpeed())
            self.flywheel_motor.set(2600)

    def spin_to_standby_speed(self):
        self.flywheel_motor.set(self.STANDBY_SPEED)

    def spin_to_geo_speed(self):
        self.flywheel_motor.set(2600)

    def spin_to_pickup_speed(self):
        self.flywheel_motor.set(2000)

    def spin_to_reverse_speed(self):
        self.flywheel_motor.set(1000)

    def spindown(self):
        self.flywheel_motor.set(0)
    
    
    def speed_increment_function(self):
        self.currentspeed=self.currentspeed+200
        self.flywheel_motor.set(self.currentspeed)
        print("Current Set Speed: ", self.currentspeed) 
    def speed_decrement_function(self):
        self.currentspeed=self.currentspeed-200
        self.flywheel_motor.set(self.currentspeed)
        print("Current Set Speed: ", self.currentspeed)



        

    


class FlywheelSensor(Sensor):
    SPEED_TOLERANCE = 50

    def __init__(self, flywheel):
        super().__init__()
        self.flywheel = flywheel

    def poll(self):
        if self.flywheel.flywheel_motor.getClosedLoopError() < self.SPEED_TOLERANCE:
            self.at_speed = True
        else:
            self.at_speed = False