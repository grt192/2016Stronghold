"""
Config File for Robot
"""

from wpilib import Solenoid, Compressor, DriverStation, CANTalon, AnalogInput

from grt.sensors.attack_joystick import Attack3Joystick
from grt.sensors.xbox_joystick import XboxJoystick
from grt.core import SensorPoller
from grt.mechanism.drivetrain import DriveTrain
from grt.mechanism.drivecontroller import ArcadeDriveController
from grt.sensors.encoder import Encoder
from grt.mechanism.mechcontroller import MechController
from grt.sensors.navx import NavX
from grt.macro.straight_macro import StraightMacro
from grt.mechanism.pickup import Pickup
from grt.mechanism.manual_shooter import ManualShooter

#Compressor initialization

c = Compressor()
c.start()

turntable_pot = AnalogInput(0)

#Manual pickup Talons and Objects

pickup_achange_motor1 = CANTalon(11)
pickup_achange_motor2 = CANTalon(7)
pickup_roller_motor = CANTalon(8)
pickup = Pickup(pickup_achange_motor1, pickup_achange_motor2, pickup_roller_motor)


#Manual shooter Talons and Objects

flywheel_motor = CANTalon(10)
shooter_act = Solenoid(1)
turntable_motor = CANTalon(12)
manual_shooter = ManualShooter(flywheel_motor, shooter_act, turntable_motor)

flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
flywheel_motor.setP(.26)
flywheel_motor.setF(.29)

#DT Talons and Objects


dt_right = CANTalon(1)
dt_r2 = CANTalon(2)
dt_r3 = CANTalon(3)
dt_left = CANTalon(4)
dt_l2 = CANTalon(5)
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



# define MechController

mc = MechController(driver_stick, xbox_controller, pickup, manual_shooter)

# define DriverStation
ds = DriverStation.getInstance()





