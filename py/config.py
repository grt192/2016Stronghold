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
from record_controller import RecordMacro, PlaybackMacro

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
dt_l2.set(4)
dt_l3.set(4)

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
instructions = OrderedDict([("7, <class 'wpilib.cantalon.CANTalon'>", [{'timeDurMs': 100, 'velocity': 0, 'zeroPos': True, 'position': -5550}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -5550}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -5550}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -5550}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -5550}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -5550}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -5550}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -5552}, {'timeDurMs': 100, 'velocity': -93, 'zeroPos': False, 'position': -5716}, {'timeDurMs': 100, 'velocity': -140, 'zeroPos': False, 'position': -5875}, {'timeDurMs': 100, 'velocity': -197, 'zeroPos': False, 'position': -6268}, {'timeDurMs': 100, 'velocity': -199, 'zeroPos': False, 'position': -6467}, {'timeDurMs': 100, 'velocity': -199, 'zeroPos': False, 'position': -6868}, {'timeDurMs': 100, 'velocity': -197, 'zeroPos': False, 'position': -7063}, {'timeDurMs': 100, 'velocity': -186, 'zeroPos': False, 'position': -7436}, {'timeDurMs': 100, 'velocity': -180, 'zeroPos': False, 'position': -7618}, {'timeDurMs': 100, 'velocity': -176, 'zeroPos': False, 'position': -7978}, {'timeDurMs': 100, 'velocity': -179, 'zeroPos': False, 'position': -8158}, {'timeDurMs': 100, 'velocity': -71, 'zeroPos': False, 'position': -8297}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -8297}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': -8297}]), ("1, <class 'wpilib.cantalon.CANTalon'>", [{'timeDurMs': 100, 'velocity': 0, 'zeroPos': True, 'position': 36221}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 36221}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 36221}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 36221}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 36221}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 36221}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 36221}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 36222}, {'timeDurMs': 100, 'velocity': 159, 'zeroPos': False, 'position': 36505}, {'timeDurMs': 100, 'velocity': 252, 'zeroPos': False, 'position': 36809}, {'timeDurMs': 100, 'velocity': 379, 'zeroPos': False, 'position': 37567}, {'timeDurMs': 100, 'velocity': 381, 'zeroPos': False, 'position': 37954}, {'timeDurMs': 100, 'velocity': 380, 'zeroPos': False, 'position': 38718}, {'timeDurMs': 100, 'velocity': 380, 'zeroPos': False, 'position': 39100}, {'timeDurMs': 100, 'velocity': 380, 'zeroPos': False, 'position': 39872}, {'timeDurMs': 100, 'velocity': 384, 'zeroPos': False, 'position': 40261}, {'timeDurMs': 100, 'velocity': 388, 'zeroPos': False, 'position': 41038}, {'timeDurMs': 100, 'velocity': 382, 'zeroPos': False, 'position': 41422}, {'timeDurMs': 100, 'velocity': 143, 'zeroPos': False, 'position': 41722}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 41722}, {'timeDurMs': 100, 'velocity': 0, 'zeroPos': False, 'position': 41722}])])
playback_macro = PlaybackMacro(instructions, [dt_left, dt_right])




# define MechController

mc = MechController(driver_stick, xbox_controller, record_macro, playback_macro, pickup)

# define DriverStation
ds = DriverStation.getInstance()





