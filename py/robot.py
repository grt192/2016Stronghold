import platform
if "Linux" in platform.platform():
    with open("/home/lvuser/py/grt/vision/camscript_new.py") as f:
        code = compile(f.read(), "/home/lvuser/py/grt/vision/camscript_new.py", 'exec')
        exec(code)

import wpilib
import time
from wpilib import SendableChooser, SmartDashboard
import numpy as np

#import print_echoer


class MyRobot(wpilib.SampleRobot):
    def __init__(self):
        super().__init__()
        import config
        # print("Imported config")
        self.hid_sp = config.hid_sp
        self.ds = config.ds
        self.navx = config.navx
        self.switch_panel = config.switch_panel
        self.flywheel_motor = config.flywheel_motor
        self.shooter = config.shooter
        self.robot_vision = config.robot_vision
        # print("done robot_vision")
        self.has_initialized = True
        #h_lower = 123
        #self.prefs = Preferences.getInstance()
        #self.prefs.putFloat("HLower2", h_lower)
        self.talon_log_arr = config.talon_log_arr

        # print("before Sendable chooser")
        self.autoChooser = SendableChooser()
        self.autoChooser.addDefault("Basic Auto", -1)
        self.autoChooser.addObject("One Bin Steal", 0)
        self.autoChooser.addObject("Two Bin Steal", 1)
        self.autoChooser.addObject("Backup Bin Steal", 2)
        SmartDashboard.putDouble("HLower", self.robot_vision.getLowerThreshold()[0])
        SmartDashboard.putDouble("SLower", self.robot_vision.getLowerThreshold()[1])
        SmartDashboard.putDouble("VLower", self.robot_vision.getLowerThreshold()[2])
        SmartDashboard.putDouble("HUpper", self.robot_vision.getUpperThreshold()[0])
        SmartDashboard.putDouble("SUpper", self.robot_vision.getUpperThreshold()[1])
        SmartDashboard.putDouble("VUpper", self.robot_vision.getUpperThreshold()[2])

        SmartDashboard.putDouble("TURNTABLE_KP", self.shooter.turntable.TURNTABLE_KP)

        SmartDashboard.putNumber("Requested Talon", 0)

        SmartDashboard.putData("Autonomous Mode", self.autoChooser)
        # print("after smartdashboard")
        #SmartDashboard.putDouble("HLower: ", h_lower)


    def disabled(self):
        i2 = 0
        while self.isDisabled():
            tinit = time.time()
            self.hid_sp.poll()
            i2 += 1
            for i in range(1, 12):
                key = "S" + str(i)
                SmartDashboard.putBoolean(key, self.switch_panel.j.getRawButton(i))
            index = int(SmartDashboard.getNumber("Requested Talon"))
            try:
                #SmartDashboard.putNumber("Output Talon", self.talon_log_arr[index].getOutputCurrent())
                SmartDashboard.putNumber("Output Talon", i2)
            except IndexError:
                pass
           
            h_lower = SmartDashboard.getDouble("HLower")
            s_lower = SmartDashboard.getDouble("SLower")
            v_lower = SmartDashboard.getDouble("VLower")
            h_upper = SmartDashboard.getDouble("HUpper")
            s_upper = SmartDashboard.getDouble("SUpper")
            v_upper = SmartDashboard.getDouble("VUpper")

            print("Rotational Error : ", self.robot_vision.rotational_error, "Vertical Error: ", self.robot_vision.vertical_error)
            self.robot_vision.rotational_error += 20

            self.robot_vision.setThreshold(np.array([h_lower, s_lower, v_lower], 'uint8'), np.array([h_upper, s_upper, v_upper], 'uint8'))
            self.shooter.turntable.TURNTABLE_KP = SmartDashboard.getDouble("TURNTABLE_KP")
            self.safeSleep(tinit, .04)
    
    def autonomous(self):
        pass
    
    def operatorControl(self):
        while self.isOperatorControl() and self.isEnabled():
            tinit = time.time()
            self.hid_sp.poll()
            #print("Target View: ", self.robot_vision.getTargetView(), "    Rotational error: ", self.robot_vision.getRotationalError())
            #print("Flywheel actual speed: ", self.flywheel_motor.getEncVelocity(), "    Flywheel set speed: ", self.shooter.flywheel.currentspeed)
            #print("Target View: ", self.robot_vision.getTargetView(), "    Rotational error: ", self.robot_vision.getRotationalError(), "    Vertical Error: ", self.robot_vision.getTargetAngle(), "    Actual Speed: ", self.flywheel_motor.getEncVelocity(), "    Set speed: ", self.shooter.flywheel.currentspeed)
            print("Rotational Error : ", self.robot_vision.rotational_error, "Vertical Error: ", self.robot_vision.vertical_error)
            self.robot_vision.rotational_error += 20
            self.safeSleep(tinit, .04)
            
    def safeSleep(self, tinit, duration):
        tdif = .04 - (time.time() - tinit)
        if tdif > 0:
            time.sleep(tdif)
        if tdif <= 0:
            print("Code running slowly!")


if __name__ == "__main__":
    print("running robot")
    wpilib.run(MyRobot)
