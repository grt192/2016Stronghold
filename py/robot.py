import platform
if "Linux" in platform.platform():
    with open("/home/lvuser/py/grt/vision/camscript_new.py") as f:
        code = compile(f.read(), "/home/lvuser/py/grt/vision/camscript_new.py", 'exec')
        exec(code)

import wpilib
import time, math
import threading
from wpilib import SendableChooser, SmartDashboard



class MyRobot(wpilib.SampleRobot):
    def __init__(self):
        super().__init__()
        import config
        self.hid_sp = config.hid_sp
        self.nt_sp = config.nt_sp
        self.one_cross_auto = config.one_cross_auto
        self.navx = config.navx
        self.shooter = config.shooter
        self.pickup = config.pickup

        self.autoChooser = SendableChooser()
        self.autoChooser.addDefault("No Autonomous", None)
        self.autoChooser.addObject("One Cross Auto", self.one_cross_auto)
        SmartDashboard.putData("Autonomous Mode", self.autoChooser)
        self.auto = self.autoChooser.getSelected()
        



    def disabled(self):
        if self.auto:
            self.auto.stop_autonomous()
        while self.isDisabled():
            tinit = time.time()
            self.hid_sp.poll()
            self.nt_sp.poll()
            self.auto = self.autoChooser.getSelected()
            
            self.safeSleep(tinit, .04)
    
    def autonomous(self):
        if self.auto:
            self.auto.run_autonomous()
        while self.isAutonomous() and self.isEnabled():
            tinit = time.time()
            self.hid_sp.poll()
            self.safeSleep(tinit, .04)
        if self.auto:
            self.auto.stop_autonomous()
        
    
    def operatorControl(self):
        if self.auto:
            self.auto.stop_autonomous()
        while self.isOperatorControl() and self.isEnabled():
            tinit = time.time()
            self.hid_sp.poll()
            #print("Pickup achange output: ", self.pickup.achange_motor_1.getOutputVoltage())
            #print("Hood motor output: ", self.shooter.hood.hood_motor.getOutputVoltage())
            #print("Target View: ", self.robot_vision.getTargetView(), "    Rotational error: ", self.robot_vision.getRotationalError())
            #print("Flywheel actual speed: ", self.flywheel_motor.getEncVelocity(), "    Flywheel set speed: ", self.shooter.flywheel.currentspeed)
            print("Target View: ", self.shooter.robot_vision.target_view, "    Rotational error: ", self.shooter.robot_vision.rotational_error, "    Vertical Error: ", self.shooter.robot_vision.vertical_error, "    Actual Speed: ", self.shooter.flywheel.flywheel_motor.getEncVelocity(), "    Set speed: ", self.shooter.flywheel.STANDBY_SPEED)
            self.safeSleep(tinit, .04)
            
    def safeSleep(self, tinit, duration):
        tdif = .04 - (time.time() - tinit)
        if tdif > 0:
            time.sleep(tdif)
        if tdif <= 0:
            print("Code running slowly!")


if __name__ == "__main__":
    wpilib.run(MyRobot)
