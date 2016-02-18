import platform
if "Linux" in platform.platform():
    with open("/home/lvuser/py/grt/vision/camscript_new.py") as f:
        code = compile(f.read(), "/home/lvuser/py/grt/vision/camscript_new.py", 'exec')
        exec(code)

import wpilib
import time

from wpilib import SmartDashboard
import numpy as np


class MyRobot(wpilib.SampleRobot):
    def __init__(self):
        super().__init__()
        import config
        self.hid_sp = config.hid_sp
        self.ds = config.ds
        self.navx = config.navx
        self.vision_sensor = config.vision_sensor
        self.robot_vision = config.robot_vision
        SmartDashboard.putDouble("HLower", self.robot_vision.getLowerThreshold()[0])
        SmartDashboard.putDouble("SLower", self.robot_vision.getLowerThreshold()[1])
        SmartDashboard.putDouble("VLower", self.robot_vision.getLowerThreshold()[2])
        SmartDashboard.putDouble("HUpper", self.robot_vision.getUpperThreshold()[0])
        SmartDashboard.putDouble("SUpper", self.robot_vision.getUpperThreshold()[1])
        SmartDashboard.putDouble("VUpper", self.robot_vision.getUpperThreshold()[2])

    def disabled(self):
        while self.isDisabled():
            tinit = time.time()
            self.hid_sp.poll()
            h_lower = SmartDashboard.getDouble("HLower")
            s_lower = SmartDashboard.getDouble("SLower")
            v_lower = SmartDashboard.getDouble("VLower")
            h_upper = SmartDashboard.getDouble("HUpper")
            s_upper = SmartDashboard.getDouble("SUpper")
            v_upper = SmartDashboard.getDouble("VUpper")

            self.robot_vision.setThreshold(np.array([h_lower, s_lower, v_lower], 'uint8'), np.array([h_upper, s_upper, v_upper], 'uint8'))
            self.safeSleep(tinit, .04)
    
    def autonomous(self):
        pass
    
    def operatorControl(self):
        while self.isOperatorControl() and self.isEnabled():
            tinit = time.time()
            self.hid_sp.poll()

            print("Target View:", self.robot_vision.target_view,
                  "Rotational Error:", self.robot_vision.rotational_error,
                  "Vertical Error:", self.robot_vision.vertical_error)

            self.safeSleep(tinit, .04)
            
    def safeSleep(self, tinit, duration):
        tdif = .04 - (time.time() - tinit)
        if tdif > 0:
            time.sleep(tdif)
        if tdif <= 0:
            print("Code running slowly!")


if __name__ == "__main__":
    wpilib.run(MyRobot)
