"""
Config File for Robot
"""

#@dhruv_rajan is editing config.py
from wpilib import Solenoid, Compressor, DriverStation, CANTalon

from grt.sensors.attack_joystick import Attack3Joystick
from grt.sensors.xbox_joystick import XboxJoystick
from grt.mechanism.flywheel import Flywheel
#from grt.sensors.gyro import Gyro
from grt.core import SensorPoller
from grt.mechanism.drivetrain import DriveTrain
from grt.mechanism.drivecontroller import ArcadeDriveController
from grt.mechanism.motorset import Motorset
from grt.sensors.ticker import Ticker
from grt.sensors.encoder import Encoder
#from grt.sensors.talon import Talon
from grt.mechanism.mechcontroller import MechController

#from grt.vision.robot_vision import Vision
#from grt.sensors.vision_sensor import VisionSensor
#from grt.mechanism.shooter import Shooter
from grt.sensors.navx import NavX
#from grt.macro.new_turn_macro import NewTurnMacro
from grt.macro.straight_macro import StraightMacro

using_vision_server = False


#from vision.robot_vision_dynamic import Vision

#vision = Vision()
#import cv2
#

navx = NavX()

#DT Talons and Objects

dt_right = CANTalon(1)
dt_r2 = CANTalon(2)
dt_left = CANTalon(7)
dt_l2 = CANTalon(8)


dt_r2.changeControlMode(CANTalon.ControlMode.Follower)
dt_l2.changeControlMode(CANTalon.ControlMode.Follower)
dt_r2.set(1)
dt_l2.set(7)

dt = DriveTrain(dt_left, dt_right, left_encoder=None, right_encoder=None)

#turn_macro = NewTurnMacro(90, navx, dt)

#flywheel_motor = CANTalon(8)
#flywheel_motor2 = CANTalon(9)
#flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
#flywheel_motor.setP(.26)
#flywheel_motor.setF(.1)
#Try a TBH controller if needed
#flywheel_motor.reverseOutput(True)

#flywheel_motor2.changeControlMode(CANTalon.ControlMode.Follower)
#flywheel_motor2.set(8)

#turntable_motor = CANTalon(7)
#hood_motor = CANTalon(6)
#rails_actuator = Solenoid(2)

#belt_roller_motor = CANTalon(10)
#flywheel = Flywheel(shooter)

#vision_sensor = VisionSensor()
#robot_vision = Vision()
#if using_vision_server:
#	import grt.vision.vision_server
#	grt.vision.vision_server.prepare_module(robot_vision)
#vision_server = VisionServer(robot_vision)

#shooter = Shooter(robot_vision, flywheel_motor, turntable_motor, hood_motor, rails_actuator, dt)





#Skeleton sensor poller
#gyro = Gyro(1)
# define sensor poller
# sp = SensorPoller()

straight_macro = StraightMacro(dt, navx)
# Drive Controllers
driver_stick = Attack3Joystick(0)
xbox_controller = XboxJoystick(1)
ac = ArcadeDriveController(dt, driver_stick, straight_macro)
hid_sp = SensorPoller((driver_stick, xbox_controller, navx))  # human interface devices



# Mech Talons, objects, and controller

# define MechController
# mc = MechController(driver_stick, xbox_controller)

# define DriverStation
ds = DriverStation.getInstance()





