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
from grt.vision.robot_vision import Vision
from grt.mechanism.shooter import Shooter
from grt.mechanism.operation_manager import OperationManager
from grt.sensors.switch_panel import SwitchPanel
from grt.macro.record_macro import RecordMacro
from grt.mechanism.override_manager import OverrideManager

using_vision_server = True

#Compressor initialization
compressor = Compressor()
compressor.start()

turntable_pot = AnalogInput(0)




#DT talons and objects
dt_right = CANTalon(1)
dt_r2 = CANTalon(2)
dt_r3 = CANTalon(3)
dt_left = CANTalon(11)
dt_l2 = CANTalon(12)
dt_l3 = CANTalon(13)
dt_shifter = Solenoid(0)


dt_r2.changeControlMode(CANTalon.ControlMode.Follower)
dt_r3.changeControlMode(CANTalon.ControlMode.Follower)
dt_l2.changeControlMode(CANTalon.ControlMode.Follower)
dt_l3.changeControlMode(CANTalon.ControlMode.Follower)
dt_r2.set(dt_right.getDeviceID())
dt_r3.set(dt_right.getDeviceID())
dt_l2.set(dt_left.getDeviceID())
dt_l3.set(dt_left.getDeviceID())

dt = DriveTrain(dt_left, dt_right, left_shifter=dt_shifter, left_encoder=None, right_encoder=None)

#Joysticks
driver_stick = Attack3Joystick(0)
xbox_controller = XboxJoystick(1)
switch_panel = SwitchPanel(2)


#Shooter Talons and Objects
flywheel_motor = CANTalon(10)
flywheel_motor2 = CANTalon(4)
flywheel_motor2.changeControlMode(CANTalon.ControlMode.Follower)
flywheel_motor2.set(flywheel_motor.getDeviceID())

flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
flywheel_motor.setPID(.33, 0, 0, f=.19)

shooter_act = Solenoid(1)

#See about configuring a max output voltage

turntable_motor = CANTalon(5)
turntable_motor.setFeedbackDevice(CANTalon.FeedbackDevice.AnalogPot)
turntable_motor.setPID(.01, 0, 0, f=0)
turntable_motor.changeControlMode(CANTalon.ControlMode.Position)


hood_motor = CANTalon(6)
hood_motor.setFeedbackDevice(CANTalon.FeedbackDevice.AnalogPot)
hood_motor.setPID(.1, 0, 0, f=0)
hood_motor.changeControlMode(CANTalon.ControlMode.Position)

robot_vision = Vision()
if using_vision_server:
	import grt.vision.vision_server
	grt.vision.vision_server.prepare_module(robot_vision)
shooter = Shooter(robot_vision, flywheel_motor, turntable_motor, hood_motor, shooter_act)


#Magic numbers for shooting:
#Raise the hood to 35 degrees (potentiometer position 247)
#Set the flywheel speed to 2600 ticks
#Check these numbers with the google spreadsheet
#Also see about adding in automatic alignment/chival de fris macro/ light-sensor-controlled pickup


#Pickup Talons and Objects
pickup_achange_motor1 = CANTalon(8)
pickup_achange_motor2 = CANTalon(7)



pickup_roller_motor = CANTalon(9)


pickup_achange_motor1.changeControlMode(CANTalon.ControlMode.Position)
pickup_achange_motor1.setFeedbackDevice(CANTalon.FeedbackDevice.AnalogPot)
pickup_achange_motor1.setPID(.01, 0, 0, f=0)
pickup_achange_motor2.changeControlMode(CANTalon.ControlMode.Position)
pickup_achange_motor2.setFeedbackDevice(CANTalon.FeedbackDevice.AnalogPot)
pickup_achange_motor2.setPID(.01, 0, 0, f=0)

pickup = Pickup(pickup_achange_motor1, pickup_achange_motor2, pickup_roller_motor)


#Straight macro initialization
navx = NavX()
straight_macro = StraightMacro(dt, navx)

#Record macro initialization
talon_arr = [dt_left, dt_right, pickup_achange_motor1, pickup_achange_motor2, pickup_roller_motor]
record_macro = RecordMacro(talon_arr)

#Operation manager, controllers, and sensor pollers
operation_manager = OperationManager(shooter, pickup, straight_macro)
override_manager = OverrideManager(shooter, pickup, compressor)
hid_sp = SensorPoller((driver_stick, xbox_controller, switch_panel, shooter.flywheel_sensor, shooter.turntable_sensor, shooter.hood_sensor, navx))
ac = ArcadeDriveController(dt, driver_stick, record_macro, operation_manager)
mc = MechController(driver_stick, xbox_controller, switch_panel, pickup, shooter, operation_manager, override_manager)

talon_log_arr = [dt_left, dt_l2, dt_l3, dt_right, dt_r2, dt_r3, flywheel_motor, flywheel_motor2, hood_motor, turntable_motor, pickup_achange_motor1, pickup_achange_motor2, pickup_roller_motor]
# define DriverStation
ds = DriverStation.getInstance()





