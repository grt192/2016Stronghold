"""
Config File for Robot
"""

from wpilib import Solenoid, Compressor, DriverStation, CANTalon

from grt.core import SensorPoller
from grt.macro.straight_macro import StraightMacro
# from grt.vision.robot_vision import Vision

from grt.sensors.attack_joystick import Attack3Joystick
from grt.sensors.xbox_joystick import XboxJoystick
from grt.sensors.navx import NavX
# from grt.sensors.vision_sensor import VisionSensor

from grt.mechanism.drivetrain import DriveTrain
from grt.mechanism.drivecontroller import ArcadeDriveController
from grt.mechanism.mechcontroller import MechController
from grt.mechanism.shooter import Shooter
from grt.mechanism.pickup import Pickup
from grt.mechanism.flywheel import Flywheel
from grt.mechanism.rails import Rails
from grt.mechanism.turntable import TurnTable
from grt.mechanism.hood import Hood
from grt.mechanism.motorset import Motorset
from queue import Queue

# Initializing Listener Queue
listener_queue = Queue()

# Compressor initialization
c = Compressor()
c.start()

# Drive Train
dt_right = CANTalon(1)
dt_r2 = CANTalon(2)
dt_r3 = CANTalon(3)
dt_left = CANTalon(4)
dt_l2 = CANTalon(5)
dt_l3 = CANTalon(6)
dt_shifter = Solenoid(0)

Motorset.group((dt_right, dt_r2, dt_r3))
Motorset.group((dt_left, dt_l2, dt_l3))


dt = DriveTrain(dt_left, dt_right, left_shifter=dt_shifter, left_encoder=None, right_encoder=None)


# Vision
# vision_sensor = VisionSensor()
# robot_vision = Vision(vision_sensor)

# Manual Pickup

# pickup_angle_change_motor1 = CANTalon(11)
# pickup_angle_change_motor2 = CANTalon(7)
# pickup_roller_motor = CANTalon(8)
# pickup = Pickup(pickup_angle_change_motor1, pickup_angle_change_motor2, pickup_roller_motor)

# Manual shooter Talons and Objects

rails_actuator = Solenoid(1)
# flywheel_motor = CANTalon(10)
# turntable_motor = CANTalon(12)
# hood_motor = CANTalon(9)

# turntable = TurnTable(robot_vision, turntable_motor, dt)
# rails = Rails(rails_actuator)
# flywheel = Flywheel(robot_vision, flywheel_motor)
# hood = Hood(robot_vision, hood_motor)
#
# shooter = Shooter(robot_vision, vision_sensor, flywheel, turntable, hood, rails, vision_enabled=False)

# Gyro/Accelerometer NavX Board
navx = NavX()

# Straight macro initialization
straight_macro = StraightMacro(dt, navx)

# Drive Controllers and sensor pollers
driver_stick = Attack3Joystick(0)
xbox_controller = XboxJoystick(1)
ac = ArcadeDriveController(dt, driver_stick, straight_macro)

hid_sp = SensorPoller((driver_stick, xbox_controller, navx))

# define MechController
mc = MechController(driver_stick, xbox_controller, None, None)#pickup , shooter)

# define DriverStation
ds = DriverStation.getInstance()
