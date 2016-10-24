from wpilib import CANTalon
from grt.core import Sensor
import threading

#FRAME_POSITION = 155
#VT_POSITION = 271
#BATTER_POSITION = 200
BALL_QUALITY = 0 #0 is good, 1 is bad

if BALL_QUALITY == 1:
    VT_POSITION = 210 #35 degrees
    LONG_RANGE_VT_POSITION = 238
if BALL_QUALITY == 0:
    # VT_POSITION = 302
    # LONG_RANGE_VT_POSITION = 330
    VT_POSITION = 292
    LONG_RANGE_VT_POSITION = 270 #was 320
# MIN_POSITION = 211 #20 degrees

# MIN_POSITION_ELEVATOR_ALLOWED = 246 #No angle for this position, but this is the lowest the hood can go before the polycarb will crash into the base plate if the elevator lowers
# MAX_POSITION = 454 #63 degrees
GEO_POSITION = 198 #23 degrees

# Flagstaff
MIN_POSITION = 205 
MAX_POSITION = 419

class Hood:
    HOOD_MIN = 155
    HOOD_MAX = 385
    def __init__(self, shooter):
        self.shooter = shooter
        self.hood_motor = shooter.hood_motor
        self.robot_vision = shooter.robot_vision
        self.override_manager = None




    def go_to_vt_angle(self):
        self.enable_automatic_control()
        print("Going to vt angle")
        self.auto_set(VT_POSITION)

    def go_to_target_angle(self):
        if self.robot_vision.getTargetView():
            if self.robot_vision.getVerticalError() > 180:
                self.auto_set(LONG_RANGE_VT_POSITION)
            else:
                self.auto_set(VT_POSITION)

    def go_to_geo_angle(self):
        self.enable_automatic_control()
        print("Going to geo angle")
        self.auto_set(GEO_POSITION)

    def go_to_frame_angle(self):
        self.enable_automatic_control()
        print("Going to frame angle")
        # self.auto_set(MIN_POSITION_ELEVATOR_ALLOWED)
        self.auto_set(MIN_POSITION)
        threading.Timer(2.5, self.disable_automatic_control).start()

    def auto_set(self, angle):
        if not self.hood_motor.getControlMode() == CANTalon.ControlMode.PercentVbus:
            self.hood_motor.set(angle)
            print("Hood set to: ", angle)

    def rotate(self, power):
        if self.hood_motor.getControlMode() == CANTalon.ControlMode.PercentVbus:
            self.hood_motor.set(power)
        else:
            print("Hood motor not in PercentVbus control mode!")

    def enable_automatic_control(self):
        if not self.override_manager.hood_override:
            self.hood_motor.changeControlMode(CANTalon.ControlMode.Position)

    def disable_automatic_control(self):
        self.hood_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.hood_motor.set(0)


class HoodSensor(Sensor):
    ANGLE_TOLERANCE = 5

    def __init__(self, hood):
        super().__init__()
        self.hood = hood

    def poll(self):
        if self.hood.hood_motor.getControlMode() == CANTalon.ControlMode.PercentVbus:
            self.vertical_ready = True
        else:
            if self.hood.hood_motor.getClosedLoopError() < self.ANGLE_TOLERANCE:
                self.vertical_ready = True
            else:
                self.vertical_ready = False



