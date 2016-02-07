import wpilib
import time
import threading
from queue import Queue
from wpilib import Preferences


class MyRobot(wpilib.SampleRobot):
    def __init__(self):
        super().__init__()

        import config
        self.hid_sp = config.hid_sp
        self.ds = config.ds
        self.navx = config.navx
        self.listener_stack = config.listener_stack

    def disabled(self):
        while self.isDisabled():
            tinit = time.time()
            self.hid_sp.poll()
            # print("Pitch: " , self.navx.pitch)
            # print("Roll: ", self.navx.roll)
            # print("Yaw: ", self.navx.yaw)
            # print("Compass heading: ", self.navx.compass_heading)
            # print("Fused heading: ", self.navx.fused_heading)
            self.safeSleep(tinit, .04)
    
    def autonomous(self):
        pass
    
    def operatorControl(self):
        poll_thread = threading.Thread(target=self.loop)
        poll_thread.start()

        while self.isOperatorControl() and self.isEnabled():
            try:
                # listener, state_id, datum = self.process_stack.pop()
                sensor, listener, state_id, datum = self.listener_stack.get()
                print(state_id, datum)
                listener(sensor, state_id, datum)
            except IndexError:
                pass

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
