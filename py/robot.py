import platform
# if "Linux" in platform.platform():
#     with open("/home/lvuser/py/grt/vision/camscript_new.py") as f:
#         code = compile(f.read(), "/home/lvuser/py/grt/vision/camscript_new.py", 'exec')
#         exec(code)
import sys
sys.path.append("/Users/dhruv/anaconda/share/OpenCV/haarcascades")
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
        self.basic_auto = config.basic_auto
        self.cross_and_shoot_auto = config.cross_and_shoot_auto
        self.low_bar_auto = config.low_bar_auto
        self.low_bar_macro = config.low_bar_macro
        self.cheval_macro = config.cheval_macro
        self.navx = config.navx
        self.shooter = config.shooter
        self.pickup = config.pickup

        self.dual_low_goal = config.dual_low_goal
        

        self.autoChooser = SendableChooser()
        self.autoChooser.addObject("No Autonomous", None)
        self.autoChooser.addObject("Dual Low Goal", self.dual_low_goal)
        #self.autoChooser.addObject("Cross And Shoot Auto", self.cross_and_shoot_auto)
        #self.autoChooser.addObject("Basic Auto", self.basic_auto)
        self.autoChooser.addDefault("Low Bar Auto", self.low_bar_macro)
        self.autoChooser.addObject("Cheval Auto" , self.cheval_macro)
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
            print("Target View: ", self.shooter.robot_vision.getTargetView(), "    Rotational error: ", self.shooter.robot_vision.getRotationalError(), "    Vertical Error: ", self.shooter.robot_vision.getTargetAngle(), "    Actual Speed: ", self.shooter.flywheel.flywheel_motor.getEncVelocity(), "    Set speed: ", self.shooter.flywheel.STANDBY_SPEED)
            self.safeSleep(tinit, .04)
        if self.auto:
            self.auto.stop_autonomous()
        
    
    def operatorControl(self):
        if self.auto:
            self.auto.stop_autonomous()
        while self.isOperatorControl() and self.isEnabled():
            tinit = time.time()
            self.hid_sp.poll()
            print("Fused heading: ", self.navx.fused_heading)
            #print("Pickup achange output: ", self.pickup.achange_motor_1.getOutputVoltage())
            #print("Hood motor output: ", self.shooter.hood.hood_motor.getOutputVoltage())
            #print("Target View: ", self.robot_vision.getTargetView(), "    Rotational error: ", self.robot_vision.getRotationalError())
            #print("Flywheel actual speed: ", self.flywheel_motor.getEncVelocity(), "    Flywheel set speed: ", self.shooter.flywheel.currentspeed)
            print("Target View: ", self.shooter.robot_vision.getTargetView(), "    Rotational error: ", self.shooter.robot_vision.getRotationalError(), "    Vertical Error: ", self.shooter.robot_vision.getTargetAngle(), "    Actual Speed: ", self.shooter.flywheel.flywheel_motor.getEncVelocity(), "    Set speed: ", self.shooter.flywheel.STANDBY_SPEED)
            #print("Number of threads: ", threading.active_count())
            self.safeSleep(tinit, .04)
            
    def safeSleep(self, tinit, duration):
        tdif = .04 - (time.time() - tinit)
        if tdif > 0:
            time.sleep(tdif)
        if tdif <= 0:
            print("Code running slowly!")


if __name__ == "__main__":
    wpilib.run(MyRobot)
