"""
Config File for Robot
"""

from wpilib import Solenoid, Compressor, DriverStation, CANTalon

from grt.sensors.attack_joystick import Attack3Joystick
from grt.sensors.xbox_joystick import XboxJoystick
from grt.core import SensorPoller
from grt.mechanism.drivetrain import DriveTrain
from grt.mechanism.drivecontroller import ArcadeDriveController
from grt.sensors.encoder import Encoder
from grt.mechanism.mechcontroller import MechController
from grt.sensors.navx import NavX
from grt.macro.straight_macro import StraightMacro
from collections import OrderedDict
from grt.mechanism.pickup import Pickup
from grt.mechanism.manual_shooter import ManualShooter
from record_controller import RecordMacro, PlaybackMacro, Playback

#Compressor initialization

c = Compressor()
c.start()

#Manual pickup Talons and Objects

pickup_achange_motor1 = CANTalon(9)
pickup_achange_motor2 = CANTalon(10)

pickup_achange_motor1.changeControlMode(CANTalon.ControlMode.Follower)
pickup_achange_motor1.set(10)
pickup_achange_motor1.reverseOutput(True)

pickup_roller_motor = CANTalon(14)
pickup = Pickup(pickup_achange_motor1, pickup_achange_motor2, pickup_roller_motor)


#Manual shooter Talons and Objects

flywheel_motor = CANTalon(13)
shooter_act = Solenoid(1)
turntable_motor = CANTalon(12)
manual_shooter = ManualShooter(flywheel_motor, shooter_act, turntable_motor)


#DT Talons and Objects


dt_right = CANTalon(1)
dt_r2 = CANTalon(2)
#dt_r3 = CANTalon(3)
dt_left = CANTalon(7)
dt_l2 = CANTalon(8)
#dt_l3 = CANTalon(6)

dt_shifter = Solenoid(0)


dt_r2.changeControlMode(CANTalon.ControlMode.Follower)
#dt_r3.changeControlMode(CANTalon.ControlMode.Follower)
dt_l2.changeControlMode(CANTalon.ControlMode.Follower)
#dt_l3.changeControlMode(CANTalon.ControlMode.Follower)
dt_r2.set(1)
#dt_r3.set(1)
dt_l2.set(7)
#dt_l3.set(7)

dt = DriveTrain(dt_left, dt_right, left_shifter=dt_shifter, left_encoder=None, right_encoder=None)


#Straight macro initialization


navx = NavX()
straight_macro = StraightMacro(dt, navx)


# Drive Controllers and sensor pollers
driver_stick = Attack3Joystick(0)
xbox_controller = XboxJoystick(1)
ac = ArcadeDriveController(dt, driver_stick, straight_macro)
hid_sp = SensorPoller((driver_stick, xbox_controller, navx))

record_macro = RecordMacro([dt_left, dt_right])

# dt_left.changeControlMode(CANTalon.ControlMode.MotionProfile)
# dt_left.MotionProfileStatus.outputEnable = True
#
# dt_right.changeControlMode(CANTalon.ControlMode.MotionProfile)
# dt_right.MotionProfileStatus.outputEnable = True
#
# profilecount = 1

# with open("/home/lvuser/py/instructions.py") as f:
#     instructions = eval(f.read())
#instructions = OrderedDict([("7, <class 'wpilib.cantalon.CANTalon'>", [{'timeDurMs': 100, 'velocity': 0, 'zeroPos': True, 'position': -5550}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -5550}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -5550}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -5550}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -5550}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -5550}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -5550}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -5552}, {'timeDurMs': 100, 'velocity': -93, 'zeroPos': False, 'position': -5716}, {'timeDurMs': 100, 'velocity': -140, 'zeroPos': False, 'position': -5875}, {'timeDurMs': 100, 'velocity': -197, 'zeroPos': False, 'position': -6268}, {'timeDurMs': 100, 'velocity': -199, 'zeroPos': False, 'position': -6467}, {'timeDurMs': 100, 'velocity': -199, 'zeroPos': False, 'position': -6868}, {'timeDurMs': 100, 'velocity': -197, 'zeroPos': False, 'position': -7063}, {'timeDurMs': 100, 'velocity': -186, 'zeroPos': False, 'position': -7436}, {'timeDurMs': 100, 'velocity': -180, 'zeroPos': False, 'position': -7618}, {'timeDurMs': 100, 'velocity': -176, 'zeroPos': False, 'position': -7978}, {'timeDurMs': 100, 'velocity': -179, 'zeroPos': False, 'position': -8158}, {'timeDurMs': 100, 'velocity': -71, 'zeroPos': False, 'position': -8297}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -8297}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -8297}]), ("1, <class 'wpilib.cantalon.CANTalon'>", [{'timeDurMs': 100, 'velocity': 0, 'zeroPos': True, 'position': 36221}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 36221}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 36221}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 36221}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 36221}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 36221}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 36221}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 36222}, {'timeDurMs': 100, 'velocity': 159, 'zeroPos': False, 'position': 36505}, {'timeDurMs': 100, 'velocity': 252, 'zeroPos': False, 'position': 36809}, {'timeDurMs': 100, 'velocity': 379, 'zeroPos': False, 'position': 37567}, {'timeDurMs': 100, 'velocity': 381, 'zeroPos': False, 'position': 37954}, {'timeDurMs': 100, 'velocity': 380, 'zeroPos': False, 'position': 38718}, {'timeDurMs': 100, 'velocity': 380, 'zeroPos': False, 'position': 39100}, {'timeDurMs': 100, 'velocity': 380, 'zeroPos': False, 'position': 39872}, {'timeDurMs': 100, 'velocity': 384, 'zeroPos': False, 'position': 40261}, {'timeDurMs': 100, 'velocity': 388, 'zeroPos': False, 'position': 41038}, {'timeDurMs': 100, 'velocity': 382, 'zeroPos': False, 'position': 41422}, {'timeDurMs': 100, 'velocity': 143, 'zeroPos': False, 'position': 41722}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 41722}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 41722}])])


#instructions = OrderedDict([("7, <class 'wpilib.cantalon.CANTalon'>", [{'velocity': 0, 'position': -548, 'zeroPos': True, 'timeDurMs': 100}]), ("1, <class 'wpilib.cantalon.CANTalon'>", [{'velocity': 0, 'position': 659, 'zeroPos': True, 'timeDurMs': 100}]), (0, [{'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -29, 'position': -2216, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -192, 'position': -2644, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -191, 'position': -2874, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -191, 'position': -3104, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -190, 'position': -3332, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -190, 'position': -3789, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -189, 'position': -4017, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -188, 'position': -4243, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -189, 'position': -4470, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -183, 'position': -4915, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -177, 'position': -5128, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -179, 'position': -5343, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -177, 'position': -5557, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -178, 'position': -5984, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -178, 'position': -6199, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -179, 'position': -6413, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -181, 'position': -6633, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -30, 'position': -6812, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -6812, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -6812, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -6812, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -6812, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -6812, 'zeroPos': False, 'timeDurMs': 100}]), (1, [{'velocity': 0, 'position': -990, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -990, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -990, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -990, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -990, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -990, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -990, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -984, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 121, 'position': -794, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 290, 'position': -422, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 356, 'position': 7, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 359, 'position': 870, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 357, 'position': 1298, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 356, 'position': 1725, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 355, 'position': 2580, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 356, 'position': 3010, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 355, 'position': 3436, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 355, 'position': 3862, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 363, 'position': 4733, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 363, 'position': 5168, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 363, 'position': 5604, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 365, 'position': 6044, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 363, 'position': 6916, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 362, 'position': 7352, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 361, 'position': 7786, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 302, 'position': 8105, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 1, 'position': 8133, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': 8133, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': 8133, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': 8133, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': 8133, 'zeroPos': False, 'timeDurMs': 100}])])

#instructions = OrderedDict([("7, <class 'wpilib.cantalon.CANTalon'>", [{'timeDurMs': 100, 'velocity': 0, 'zeroPos': True, 'position': -45865}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -45865}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -45865}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -45865}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -45865}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -45865}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -45865}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -45865}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -45865}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -45865}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -45865}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -45865}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -45865}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -45866}, {'timeDurMs': 100, 'velocity': -18, 'zeroPos': False, 'position': -45899}, {'timeDurMs': 100, 'velocity': -299, 'zeroPos': False, 'position': -46467}, {'timeDurMs': 100, 'velocity': -410, 'zeroPos': False, 'position': -46965}, {'timeDurMs': 100, 'velocity': -424, 'zeroPos': False, 'position': -47477}, {'timeDurMs': 100, 'velocity': -426, 'zeroPos': False, 'position': -47988}, {'timeDurMs': 100, 'velocity': -426, 'zeroPos': False, 'position': -49011}, {'timeDurMs': 100, 'velocity': -423, 'zeroPos': False, 'position': -49519}, {'timeDurMs': 100, 'velocity': -422, 'zeroPos': False, 'position': -50027}, {'timeDurMs': 100, 'velocity': -423, 'zeroPos': False, 'position': -50535}, {'timeDurMs': 100, 'velocity': -421, 'zeroPos': False, 'position': -51547}, {'timeDurMs': 100, 'velocity': -414, 'zeroPos': False, 'position': -52043}, {'timeDurMs': 100, 'velocity': -413, 'zeroPos': False, 'position': -52539}, {'timeDurMs': 100, 'velocity': -412, 'zeroPos': False, 'position': -53034}, {'timeDurMs': 100, 'velocity': -411, 'zeroPos': False, 'position': -54024}, {'timeDurMs': 100, 'velocity': -411, 'zeroPos': False, 'position': -54518}, {'timeDurMs': 100, 'velocity': -411, 'zeroPos': False, 'position': -55012}, {'timeDurMs': 100, 'velocity': -410, 'zeroPos': False, 'position': -55505}, {'timeDurMs': 100, 'velocity': -411, 'zeroPos': False, 'position': -56492}, {'timeDurMs': 100, 'velocity': -410, 'zeroPos': False, 'position': -56983}, {'timeDurMs': 100, 'velocity': -409, 'zeroPos': False, 'position': -57475}, {'timeDurMs': 100, 'velocity': -410, 'zeroPos': False, 'position': -57968}, {'timeDurMs': 100, 'velocity': -409, 'zeroPos': False, 'position': -58952}, {'timeDurMs': 100, 'velocity': -410, 'zeroPos': False, 'position': -59446}, {'timeDurMs': 100, 'velocity': -409, 'zeroPos': False, 'position': -59938}, {'timeDurMs': 100, 'velocity': -410, 'zeroPos': False, 'position': -60430}, {'timeDurMs': 100, 'velocity': -409, 'zeroPos': False, 'position': -61415}, {'timeDurMs': 100, 'velocity': -410, 'zeroPos': False, 'position': -61908}, {'timeDurMs': 100, 'velocity': -410, 'zeroPos': False, 'position': -62401}, {'timeDurMs': 100, 'velocity': -410, 'zeroPos': False, 'position': -62893}, {'timeDurMs': 100, 'velocity': -410, 'zeroPos': False, 'position': -63878}, {'timeDurMs': 100, 'velocity': -409, 'zeroPos': False, 'position': -64370}, {'timeDurMs': 100, 'velocity': -410, 'zeroPos': False, 'position': -64863}, {'timeDurMs': 100, 'velocity': -410, 'zeroPos': False, 'position': -65355}, {'timeDurMs': 100, 'velocity': -393, 'zeroPos': False, 'position': -66307}, {'timeDurMs': 100, 'velocity': -237, 'zeroPos': False, 'position': -66525}, {'timeDurMs': 100, 'velocity': -14, 'zeroPos': False, 'position': -66533}]), ("1, <class 'wpilib.cantalon.CANTalon'>", [{'timeDurMs': 100, 'velocity': 0, 'zeroPos': True, 'position': 118820}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 118820}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 118820}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 118820}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 118820}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 118820}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 118820}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 118820}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 118820}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 118820}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 118820}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 118820}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 118820}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 118822}, {'timeDurMs': 100, 'velocity': 15, 'zeroPos': False, 'position': 118851}, {'timeDurMs': 100, 'velocity': 202, 'zeroPos': False, 'position': 119228}, {'timeDurMs': 100, 'velocity': 260, 'zeroPos': False, 'position': 119543}, {'timeDurMs': 100, 'velocity': 267, 'zeroPos': False, 'position': 119863}, {'timeDurMs': 100, 'velocity': 264, 'zeroPos': False, 'position': 120182}, {'timeDurMs': 100, 'velocity': 278, 'zeroPos': False, 'position': 120840}, {'timeDurMs': 100, 'velocity': 303, 'zeroPos': False, 'position': 121213}, {'timeDurMs': 100, 'velocity': 331, 'zeroPos': False, 'position': 121614}, {'timeDurMs': 100, 'velocity': 346, 'zeroPos': False, 'position': 122031}, {'timeDurMs': 100, 'velocity': 356, 'zeroPos': False, 'position': 122881}, {'timeDurMs': 100, 'velocity': 358, 'zeroPos': False, 'position': 123311}, {'timeDurMs': 100, 'velocity': 358, 'zeroPos': False, 'position': 123740}, {'timeDurMs': 100, 'velocity': 358, 'zeroPos': False, 'position': 124170}, {'timeDurMs': 100, 'velocity': 356, 'zeroPos': False, 'position': 125026}, {'timeDurMs': 100, 'velocity': 358, 'zeroPos': False, 'position': 125458}, {'timeDurMs': 100, 'velocity': 360, 'zeroPos': False, 'position': 125891}, {'timeDurMs': 100, 'velocity': 357, 'zeroPos': False, 'position': 126320}, {'timeDurMs': 100, 'velocity': 356, 'zeroPos': False, 'position': 127176}, {'timeDurMs': 100, 'velocity': 357, 'zeroPos': False, 'position': 127604}, {'timeDurMs': 100, 'velocity': 356, 'zeroPos': False, 'position': 128032}, {'timeDurMs': 100, 'velocity': 358, 'zeroPos': False, 'position': 128462}, {'timeDurMs': 100, 'velocity': 357, 'zeroPos': False, 'position': 129323}, {'timeDurMs': 100, 'velocity': 356, 'zeroPos': False, 'position': 129751}, {'timeDurMs': 100, 'velocity': 355, 'zeroPos': False, 'position': 130177}, {'timeDurMs': 100, 'velocity': 356, 'zeroPos': False, 'position': 130604}, {'timeDurMs': 100, 'velocity': 356, 'zeroPos': False, 'position': 131460}, {'timeDurMs': 100, 'velocity': 360, 'zeroPos': False, 'position': 131891}, {'timeDurMs': 100, 'velocity': 356, 'zeroPos': False, 'position': 132318}, {'timeDurMs': 100, 'velocity': 355, 'zeroPos': False, 'position': 132744}, {'timeDurMs': 100, 'velocity': 354, 'zeroPos': False, 'position': 133598}, {'timeDurMs': 100, 'velocity': 353, 'zeroPos': False, 'position': 134024}, {'timeDurMs': 100, 'velocity': 354, 'zeroPos': False, 'position': 134450}, {'timeDurMs': 100, 'velocity': 359, 'zeroPos': False, 'position': 134882}, {'timeDurMs': 100, 'velocity': 320, 'zeroPos': False, 'position': 135655}, {'timeDurMs': 100, 'velocity': 69, 'zeroPos': False, 'position': 135702}, {'timeDurMs': 100, 'velocity': 1, 'zeroPos': False, 'position': 135704}])])

instructions = OrderedDict([("7, <class 'wpilib.cantalon.CANTalon'>", [{'position': -82930, 'timeDurMs': 100, 'zeroPos': True, 'velocity': 0}, {'position': -83905, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': -83905, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': -83905, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': -83905, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': -83905, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': -83883, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 13}, {'position': -83839, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 32}, {'position': -83766, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 57}, {'position': -83666, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 79}, {'position': -83408, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 113}, {'position': -83255, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 126}, {'position': -83094, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 132}, {'position': -82925, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 140}, {'position': -82566, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 150}, {'position': -82381, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 153}, {'position': -82198, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 152}, {'position': -81875, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 125}, {'position': -81780, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 86}, {'position': -81724, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 51}, {'position': -81690, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 30}, {'position': -81649, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 15}, {'position': -81635, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 12}, {'position': -81631, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 4}, {'position': -81631, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': -81631, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': -81631, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': -81631, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': -81631, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': -81631, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': -81633, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -1}, {'position': -81637, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -3}, {'position': -81643, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -5}, {'position': -81661, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -7}, {'position': -81671, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -8}, {'position': -81683, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -9}, {'position': -81694, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -9}, {'position': -81708, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -3}, {'position': -81707, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}]), ("1, <class 'wpilib.cantalon.CANTalon'>", [{'position': 108731, 'timeDurMs': 100, 'zeroPos': True, 'velocity': 0}, {'position': 105485, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': 105485, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': 105485, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': 105485, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': 105483, 'timeDurMs': 100, 'zeroPos': False, 'velocity': 0}, {'position': 105477, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -4}, {'position': 105410, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -34}, {'position': 105341, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -54}, {'position': 105252, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -71}, {'position': 105151, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -82}, {'position': 104896, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -111}, {'position': 104753, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -118}, {'position': 104604, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -123}, {'position': 104452, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -126}, {'position': 104145, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -128}, {'position': 103990, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -129}, {'position': 103837, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -127}, {'position': 103695, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -120}, {'position': 103470, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -87}, {'position': 103389, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -69}, {'position': 103320, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -58}, {'position': 103257, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -53}, {'position': 103140, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -48}, {'position': 103088, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -43}, {'position': 103037, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -42}, {'position': 102986, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -42}, {'position': 102885, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -41}, {'position': 102834, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -42}, {'position': 102784, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -42}, {'position': 102735, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -40}, {'position': 102636, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -41}, {'position': 102587, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -40}, {'position': 102536, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -42}, {'position': 102432, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -43}, {'position': 102380, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -42}, {'position': 102329, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -42}, {'position': 102281, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -41}, {'position': 102228, 'timeDurMs': 100, 'zeroPos': False, 'velocity': -16}])])


playback_macro = Playback(None, [dt_left, dt_right])




# define MechController

mc = MechController(driver_stick, xbox_controller, record_macro, playback_macro, pickup)

# define DriverStation
ds = DriverStation.getInstance()





