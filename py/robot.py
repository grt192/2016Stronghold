import wpilib
import time
import threading
from wpilib import Preferences


class MyRobot(wpilib.SampleRobot):
    def __init__(self):
        super().__init__()
        import config
        self.hid_sp = config.hid_sp
        self.ds = config.ds
        self.navx = config.navx
        self.flywheel_motor = config.flywheel_motor
        self.turntable_pot = config.turntable_pot
        self.manual_shooter = config.manual_shooter


    def disabled(self):
        while self.isDisabled():
            tinit = time.time()
            self.hid_sp.poll()
            #print("Pitch: " , self.navx.pitch)
            #print("Roll: ", self.navx.roll)
            #print("Yaw: ", self.navx.yaw)
            #print("Compass heading: ", self.navx.compass_heading)
            #print("Fused heading: ", self.navx.fused_heading)
            print("Flywheel speed: ", self.flywheel_motor.getEncVelocity())
            print("Potentiometer position: ", self.turntable_pot.getVoltage())
            self.safeSleep(tinit, .04)
    
    def autonomous(self):
        pass
    
    def operatorControl(self):
        while self.isOperatorControl() and self.isEnabled():
            tinit = time.time()
            self.hid_sp.poll()
            print("Flywheel actual speed: ", self.flywheel_motor.getEncVelocity())
            print("Flywheel set speed: ", self.manual_shooter.current_speed)
            self.safeSleep(tinit, .04)
            
    def safeSleep(self, tinit, duration):
        tdif = .04 - (time.time() - tinit)
        if tdif > 0:
            time.sleep(tdif)
        if tdif <= 0:
            print("Code running slowly!")


if __name__ == "__main__":
    wpilib.run(MyRobot)
