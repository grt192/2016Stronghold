

import wpilib
import time


class MyRobot(wpilib.SampleRobot):

    autonomousCommand = None
    autoChooser = None
    
    def __init__(self):
        super().__init__()
        import config
        self.sp = config.sp
        self.hid_sp = config.hid_sp
        self.ds = config.ds

        self.autoChooser = SendableChooser()
        self.autoChooser.addDefault("Basic Auto", BasicAuto)
        self.autoChooser.addObject("One Bin Steal", OneBinSteal)
        self.autoChooser.addObject("Two Bin Steal", TwoBinSteal)
        self.autoChooser.addObject("Backup Bin Steal", BackupBinSteal)
        self.SmartDashboard.putData("Autonomous mode chooser", self.autoChooser)

    def disabled(self):
        while self.isDisabled():
            tinit = time.time()
            self.sp.poll()
            self.safeSleep(tinit, .04)
    
    def autonomous(self):
        # define auto here
        pass
    
    def operatorControl(self):
        while self.isOperatorControl() and self.isEnabled():
            tinit = time.time()
            self.sp.poll()
            self.hid_sp.poll()
            self.safeSleep(tinit, .04)
            
    def safeSleep(self, tinit, duration):
        tdif = .04 - (time.time() - tinit)
        if tdif > 0:
            time.sleep(tdif)
        if tdif <= 0:
            print("Code running slowly!")

    def autonomousInit(self):
        self.autonomousCommand = autoChooser.getSelected()
        self.autonomousCommand.start()

    def autonomousPeriodic(self):
        Scheduler.getInstance().run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
