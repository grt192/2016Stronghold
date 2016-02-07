import wpilib
import time
import threading
from wpilib import Preferences


class MyRobot(wpilib.SampleRobot):
    def __init__(self):
        super().__init__()
        listener_stack = []
        import config
        self.process_stack = config.process_stack
        self.hid_sp = config.hid_sp
        self.ds = config.ds
        self.navx = config.navx


    def disabled(self):
        while self.isDisabled():
            tinit = time.time()
            self.hid_sp.poll()
            print("Pitch: " , self.navx.pitch)
            print("Roll: ", self.navx.roll)
            print("Yaw: ", self.navx.yaw)
            print("Compass heading: ", self.navx.compass_heading)
            print("Fused heading: ", self.navx.fused_heading)
            self.safeSleep(tinit, .04)
    
    def autonomous(self):
        pass
    
    def operatorControl(self):
        poll_thread = threading.Thread(target=self.loop)
        while self.isOperatorControl() and self.isEnabled():
            listener = self.process_stack.pop()
            listener()

    def loop(self):
        while self.isOperatorControl() and self.isEnabled():
            tinit = time.time()
            self.hid_sp.poll()
            self.safeSleep(tinit, .04)
            
    def safeSleep(self, tinit, duration):
        tdif = .04 - (time.time() - tinit)
        if tdif > 0:
            time.sleep(tdif)
        if tdif <= 0:
            print("Code running slowly!")


if __name__ == "__main__":
    wpilib.run(MyRobot)
