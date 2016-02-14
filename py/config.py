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

pickup_roller_motor = CANTalon(8)
pickup = Pickup(pickup_achange_motor1, pickup_achange_motor2, pickup_roller_motor)


#Manual shooter Talons and Objects

flywheel_motor = CANTalon(7)
shooter_act = Solenoid(1)
turntable_motor = CANTalon(12)
manual_shooter = ManualShooter(flywheel_motor, shooter_act, turntable_motor)


#DT Talons and Objects


dt_right = CANTalon(1)
dt_r2 = CANTalon(2)
dt_r3 = CANTalon(3)
dt_left = CANTalon(7)
dt_l2 = CANTalon(8)
dt_l3 = CANTalon(6)

dt_shifter = Solenoid(0)


dt_r2.changeControlMode(CANTalon.ControlMode.Follower)
dt_r3.changeControlMode(CANTalon.ControlMode.Follower)
dt_l2.changeControlMode(CANTalon.ControlMode.Follower)
dt_l3.changeControlMode(CANTalon.ControlMode.Follower)
dt_r2.set(1)
dt_r3.set(1)
dt_l2.set(7)
dt_l3.set(7)

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

instructions = OrderedDict([("7, <class 'wpilib.cantalon.CANTalon'>", [{'velocity': 0, 'position': -548, 'zeroPos': True, 'timeDurMs': 100}]), ("1, <class 'wpilib.cantalon.CANTalon'>", [{'velocity': 0, 'position': 659, 'zeroPos': True, 'timeDurMs': 100}]), (0, [{'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -2155, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -29, 'position': -2216, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -192, 'position': -2644, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -191, 'position': -2874, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -191, 'position': -3104, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -190, 'position': -3332, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -190, 'position': -3789, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -189, 'position': -4017, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -188, 'position': -4243, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -189, 'position': -4470, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -183, 'position': -4915, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -177, 'position': -5128, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -179, 'position': -5343, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -177, 'position': -5557, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -178, 'position': -5984, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -178, 'position': -6199, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -179, 'position': -6413, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -181, 'position': -6633, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': -30, 'position': -6812, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -6812, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -6812, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -6812, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -6812, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -6812, 'zeroPos': False, 'timeDurMs': 100}]), (1, [{'velocity': 0, 'position': -990, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -990, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -990, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -990, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -990, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -990, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -990, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': -984, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 121, 'position': -794, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 290, 'position': -422, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 356, 'position': 7, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 359, 'position': 870, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 357, 'position': 1298, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 356, 'position': 1725, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 355, 'position': 2580, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 356, 'position': 3010, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 355, 'position': 3436, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 355, 'position': 3862, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 363, 'position': 4733, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 363, 'position': 5168, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 363, 'position': 5604, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 365, 'position': 6044, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 363, 'position': 6916, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 362, 'position': 7352, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 361, 'position': 7786, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 302, 'position': 8105, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 1, 'position': 8133, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': 8133, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': 8133, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': 8133, 'zeroPos': False, 'timeDurMs': 100}, {'velocity': 0, 'position': 8133, 'zeroPos': False, 'timeDurMs': 100}])])

playback_macro = Playback(instructions, [dt_left, dt_right])




# define MechController

mc = MechController(driver_stick, xbox_controller, record_macro, playback_macro, pickup)

# define DriverStation
ds = DriverStation.getInstance()





