import platform
if "Linux" in platform.platform():
    with open("/home/lvuser/py/grt/vision/camscript_new.py") as f:
        code = compile(f.read(), "/home/lvuser/py/grt/vision/camscript_new.py", 'exec')
        exec(code)

import wpilib
import time, math
import threading
from wpilib import Preferences
from wpilib import SendableChooser, SmartDashboard, Preferences, LiveWindow, Sendable
import numpy as np
from networktables import NetworkTable

#import print_echoer


class MyRobot(wpilib.SampleRobot):
    def __init__(self):
        super().__init__()
        import config
        self.hid_sp = config.hid_sp
        self.ds = config.ds
        self.navx = config.navx
        self.switch_panel = config.switch_panel
        self.flywheel_motor = config.flywheel_motor
        self.turntable_pot = config.turntable_pot
        self.shooter = config.shooter
        self.pickup = config.pickup
        self.robot_vision = config.robot_vision
        self.has_initialized = True
        self.status_table = NetworkTable.getTable("Status Table")
        #h_lower = 123
        #self.prefs = Preferences.getInstance()
        #self.prefs.putFloat("HLower2", h_lower)
        self.talon_log_arr = config.talon_log_arr

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
        #SmartDashboard.putData("Turntable Re-Zero", self.shooter.turntable.re_zero)
        #SmartDashboard.putBoolean("Testing", False)
        #SmartDashboard.putDouble("HLower: ", h_lower)
        for i in range(1, len(self.talon_log_arr)+1):
                key = "Talon " + str(i) + " Current"
                #print(key)
                #self.status_table.putNumber(key, self.talon_log_arr[i].getOutputCurrent())
                self.status_table.putNumber(key, 0)


    def disabled(self):
        i2 = 0
        while self.isDisabled():
            tinit = time.time()
            self.hid_sp.poll()
            # i2 += math.pi / 16
            # for i in range(1, 12):
            #     key = "S" + str(i)
            #     SmartDashboard.putBoolean(key, self.switch_panel.j.getRawButton(i))
            # index = int(SmartDashboard.getNumber("Requested Talon"))
            # try:
            #     #SmartDashboard.putNumber("Output Talon", self.talon_log_arr[index].getOutputCurrent())
            #     SmartDashboard.putNumber("Output Talon", i2)
            # except IndexError:
            #     pass

            # self.status_table.putNumber("NumTalons", len(self.talon_log_arr))
            # for i in range(1, len(self.talon_log_arr)+1):
            #     key = "Talon " + str(i) + " Current"
            #     #print(key)
            #     #self.status_table.putNumber(key, self.talon_log_arr[i].getOutputCurrent())
            #     self.status_table.putNumber(key, (i+1) * math.sin(i2))
            self.status_table.putNumber("HoodPot", self.shooter.hood.hood_motor.getPosition())
            self.status_table.putNumber("TurntablePot", self.shooter.turntable.turntable_motor.getPosition())
            self.status_table.putNumber("PickupPot1", self.pickup.achange_motor_1.getPosition())
            self.status_table.putNumber("PickupPot2", self.pickup.achange_motor_2.getPosition())
            self.status_table.putNumber("FlywheelEncoder", self.shooter.flywheel.flywheel_motor.getEncVelocity())
            self.status_table.putNumber("RotationalError", self.shooter.robot_vision.getRotationalError())
            if self.shooter.robot_vision.getTargetView():
                self.status_table.putNumber("TargetView", 500)
            else:
                self.status_table.putNumber("TargetView", 0)

           
            # h_lower = SmartDashboard.getDouble("HLower")
            # s_lower = SmartDashboard.getDouble("SLower")
            # v_lower = SmartDashboard.getDouble("VLower")
            # h_upper = SmartDashboard.getDouble("HUpper")
            # s_upper = SmartDashboard.getDouble("SUpper")
            # v_upper = SmartDashboard.getDouble("VUpper")

            # self.robot_vision.setThreshold(np.array([h_lower, s_lower, v_lower], 'uint8'), np.array([h_upper, s_upper, v_upper], 'uint8'))
            # self.shooter.turntable.TURNTABLE_KP = SmartDashboard.getDouble("TURNTABLE_KP")
            self.safeSleep(tinit, .04)
    
    def autonomous(self):
        pass
    
    def operatorControl(self):
        while self.isOperatorControl() and self.isEnabled():
            tinit = time.time()
            self.hid_sp.poll()
            #print("Pickup achange output: ", self.pickup.achange_motor_1.getOutputVoltage())
            print("Hood motor output: ", self.shooter.hood.hood_motor.getOutputVoltage())
            #print("Target View: ", self.robot_vision.getTargetView(), "    Rotational error: ", self.robot_vision.getRotationalError())
            #print("Flywheel actual speed: ", self.flywheel_motor.getEncVelocity(), "    Flywheel set speed: ", self.shooter.flywheel.currentspeed)
            #print("Target View: ", self.robot_vision.getTargetView(), "    Rotational error: ", self.robot_vision.getRotationalError(), "    Vertical Error: ", self.robot_vision.getTargetAngle(), "    Actual Speed: ", self.flywheel_motor.getEncVelocity(), "    Set speed: ", self.shooter.flywheel.currentspeed)
            self.safeSleep(tinit, .04)
            
    def safeSleep(self, tinit, duration):
        tdif = .04 - (time.time() - tinit)
        if tdif > 0:
            time.sleep(tdif)
        if tdif <= 0:
            print("Code running slowly!")


if __name__ == "__main__":
    wpilib.run(MyRobot)
