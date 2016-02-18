import platform
if "Linux" in platform.platform():
    with open("/home/lvuser/py/grt/vision/camscript_new.py") as f:
        code = compile(f.read(), "/home/lvuser/py/grt/vision/camscript_new.py", 'exec')
        exec(code)

import wpilib
import time
import threading
from wpilib import Preferences
from wpilib import SendableChooser, SmartDashboard, Preferences, LiveWindow
import numpy as np

#import print_echoer


class MyRobot(wpilib.SampleRobot):
    def __init__(self):
        super().__init__()
        import config
        self.hid_sp = config.hid_sp
        self.ds = config.ds
        self.navx = config.navx
        self.flywheel_motor = config.flywheel_motor
        self.turntable_pot = config.turntable_pot
        self.shooter = config.shooter
        self.robot_vision = config.robot_vision
        self.has_initialized = True
        #h_lower = 123
        #self.prefs = Preferences.getInstance()
        #self.prefs.putFloat("HLower2", h_lower)

        #self.autoChooser = SendableChooser()
        #self.autoChooser.addDefault("Basic Auto", -1)
        #self.autoChooser.addObject("One Bin Steal", 0)
        #self.autoChooser.addObject("Two Bin Steal", 1)
        #self.autoChooser.addObject("Backup Bin Steal", 2)
        SmartDashboard.putDouble("HLower", self.robot_vision.getLowerThreshold()[0])
        SmartDashboard.putDouble("SLower", self.robot_vision.getLowerThreshold()[1])
        SmartDashboard.putDouble("VLower", self.robot_vision.getLowerThreshold()[2])
        SmartDashboard.putDouble("HUpper", self.robot_vision.getUpperThreshold()[0])
        SmartDashboard.putDouble("SUpper", self.robot_vision.getUpperThreshold()[1])
        SmartDashboard.putDouble("VUpper", self.robot_vision.getUpperThreshold()[2])

        SmartDashboard.putDouble("TURNTABLE_KP", self.shooter.turntable.TURNTABLE_KP)

        #SmartDashboard.putData("Autonomous mode chooser", self.autoChooser)
        #SmartDashboard.putDouble("HLower: ", h_lower)


    def disabled(self):
        print("Hi!!!!")
        while self.isDisabled():
            tinit = time.time()
            self.hid_sp.poll()
            #print("Pitch: " , self.navx.pitch)
            #print("Roll: ", self.navx.roll)
            #print("Yaw: ", self.navx.yaw)
            #print("Compass heading: ", self.navx.compass_heading)
            #print("Fused heading: ", self.navx.fused_heading)
            #print("Flywheel speed: ", self.flywheel_motor.getEncVelocity())
            #print("Potentiometer position: ", self.turntable_pot.getVoltage())
            print("Target View: ", self.robot_vision.getTargetView(), "    Rotational error: ", self.robot_vision.getRotationalError())
            #auto = self.autoChooser.getSelected()
            #print(auto)
            h_lower = SmartDashboard.getDouble("HLower")
            s_lower = SmartDashboard.getDouble("SLower")
            v_lower = SmartDashboard.getDouble("VLower")
            h_upper = SmartDashboard.getDouble("HUpper")
            s_upper = SmartDashboard.getDouble("SUpper")
            v_upper = SmartDashboard.getDouble("VUpper")

            self.robot_vision.setThreshold(np.array([h_lower, s_lower, v_lower], 'uint8'), np.array([h_upper, s_upper, v_upper], 'uint8'))
            self.shooter.turntable.TURNTABLE_KP = SmartDashboard.getDouble("TURNTABLE_KP")
            self.safeSleep(tinit, .04)
    
    def autonomous(self):
        pass
    
    def operatorControl(self):
        while self.isOperatorControl() and self.isEnabled():
            tinit = time.time()
            self.hid_sp.poll()
            #print("Flywheel actual speed: ", self.flywheel_motor.getEncVelocity())
            #print("Flywheel set speed: ", self.shooter.flywheel.currentspeed)
            #print("Target View: ", self.robot_vision.getTargetView(), "    Rotational error: ", self.robot_vision.getRotationalError())
            self.safeSleep(tinit, .04)
            
    def safeSleep(self, tinit, duration):
        tdif = .04 - (time.time() - tinit)
        if tdif > 0:
            time.sleep(tdif)
        if tdif <= 0:
            print("Code running slowly!")


if __name__ == "__main__":
    wpilib.run(MyRobot)
