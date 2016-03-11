"""
Config File for Robot
"""

from wpilib import Solenoid, Compressor, DriverStation, CANTalon, AnalogInput
from grt.sensors.switch import Switch

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
from grt.macro.pickup_macro import PickupMacro
from grt.sensors.switch_panel import SwitchPanel
from grt.macro.record_macro import RecordMacro, PlaybackMacro
from grt.mechanism.override_manager import OverrideManager

from grt.autonomous.basic_auto import BasicAuto
from grt.autonomous.cross_and_shoot_auto import CrossAndShootAuto


from grt.mechanism.nt_ticker import NTTicker
from collections import OrderedDict

using_vision_server = True





#Compressor initialization
compressor = Compressor()
compressor.start()

turntable_pot = AnalogInput(0)




#DT talons and objects

dt_right = CANTalon(1)
# dt_r2 = CANTalon(2)
# dt_r3 = CANTalon(3)
dt_left = CANTalon(11)
# dt_l2 = CANTalon(12)
# dt_l3 = CANTalon(13)
dt_shifter = Solenoid(0)


# dt_r2.changeControlMode(CANTalon.ControlMode.Follower)
# dt_r3.changeControlMode(CANTalon.ControlMode.Follower)
# dt_l2.changeControlMode(CANTalon.ControlMode.Follower)
# dt_l3.changeControlMode(CANTalon.ControlMode.Follower)
# dt_r2.set(dt_right.getDeviceID())
# dt_r3.set(dt_right.getDeviceID())
# dt_l2.set(dt_left.getDeviceID())
# dt_l3.set(dt_left.getDeviceID())

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
#flywheel_motor.setPID(.33, 0, 0, f=.19) #Omega 1 tuning constants
flywheel_motor.setPID(.33, 0, 0, f=.3) #Omega 2 tuning constants

shooter_act = Solenoid(1)

#See about configuring a max output voltage

turntable_motor = CANTalon(5)
turntable_motor.setFeedbackDevice(CANTalon.FeedbackDevice.AnalogPot)
turntable_motor.setPID(90, 0, 0, f=0)
turntable_motor.configMaxOutputVoltage(8)
turntable_motor.setAllowableClosedLoopErr(2)
turntable_motor.reverseOutput(False)
turntable_motor.changeControlMode(CANTalon.ControlMode.Position)


hood_motor = CANTalon(6)
hood_motor.setFeedbackDevice(CANTalon.FeedbackDevice.AnalogPot)
hood_motor.setPID(10, 0, 0, f=0)
hood_motor.configMaxOutputVoltage(5)
hood_motor.setAllowableClosedLoopErr(5)
hood_motor.changeControlMode(CANTalon.ControlMode.Position)

robot_vision = Vision()
if using_vision_server:
	import grt.vision.vision_server
	grt.vision.vision_server.prepare_module(robot_vision)
shooter = Shooter(robot_vision, flywheel_motor, turntable_motor, hood_motor, shooter_act)


ball_switch = Switch(0)

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
pickup_achange_motor1.setPID(16, 0, 0, f=0)
pickup_achange_motor1.setAllowableClosedLoopErr(5)
pickup_achange_motor2.changeControlMode(CANTalon.ControlMode.Position)
pickup_achange_motor2.setFeedbackDevice(CANTalon.FeedbackDevice.AnalogPot)
pickup_achange_motor2.setPID(20, 0, 0, f=0)
pickup_achange_motor2.setAllowableClosedLoopErr(5)


pickup = Pickup(pickup_achange_motor1, pickup_achange_motor2, pickup_roller_motor)


#Straight macro initialization
navx = NavX()
straight_macro = StraightMacro(dt, navx)
# one_cross_auto = OneCrossAuto(straight_macro)

# Macros

#Record macro initialization
talon_arr = [dt_left, dt_right, pickup_achange_motor1, pickup_achange_motor2, pickup_roller_motor]
record_macro = RecordMacro(talon_arr)
#sim_instructions = OrderedDict([("11, <class 'wpilib.cantalon.CANTalon'>", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798]), ("1, <class 'wpilib.cantalon.CANTalon'>", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798]), ("8, <class 'wpilib.cantalon.CANTalon'>", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), ("9, <class 'wpilib.cantalon.CANTalon'>", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), ("7, <class 'wpilib.cantalon.CANTalon'>", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])])
shop_instructions = OrderedDict([("11, <class 'wpilib.cantalon.CANTalon'>", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.08504398826979472, 0.10068426197458455, 0.24144672531769307, 0.4447702834799609, 0.3118279569892473, 0.14760508308895406, 0.04594330400782014, 0.04594330400782014, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06158357771260997, 0.06158357771260997, 0.0, 0.0, 0.0, 0.0, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), ("1, <class 'wpilib.cantalon.CANTalon'>", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.08504398826979472, -0.10068426197458455, -0.2649071358748778, -0.3196480938416422, -0.13978494623655913, 0.022482893450635387, -0.04594330400782014, -0.04594330400782014, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.06158357771260997, -0.06158357771260997, 0.0, 0.0, 0.0, 0.0, -0.6999022482893451, -0.6999022482893451, -0.6999022482893451, -0.6999022482893451, -0.6999022482893451, -0.6999022482893451, -0.6999022482893451, -0.6999022482893451, -0.6999022482893451, -0.6999022482893451, -0.6999022482893451, -0.6999022482893451, 0.0, 0.0, 0.0, 0.0, 0.0]), ("8, <class 'wpilib.cantalon.CANTalon'>", [0.02346041055718475, 0.03128054740957967, 0.03128054740957967, 0.02346041055718475, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03128054740957967, 0.03128054740957967, 0.03128054740957967, 0.02346041055718475, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.9843597262952102, -0.9843597262952102, -0.9843597262952102, -0.9843597262952102, 0.03128054740957967, 1.0, 1.0, 0.0, 0.0, 0.0, 0.833822091886608, 1.0, 1.0, 0.739980449657869, 0.14076246334310852, 0.14076246334310852, 0.14076246334310852, 0.12512218963831867, 0.12512218963831867, 0.12512218963831867, 0.12512218963831867, 0.12512218963831867, 0.10948191593352884, 0.093841642228739, 0.093841642228739, 0.093841642228739, 0.07820136852394917, 0.06256109481915934, 0.02346041055718475, 0.007820136852394917, -0.7810361681329423, -0.9765395894428153, -0.9765395894428153, -0.9765395894428153, -0.9765395894428153, 0.0, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997, -0.06158357771260997]), ("9, <class 'wpilib.cantalon.CANTalon'>", [-0.02346041055718475, -0.03128054740957967, -0.03128054740957967, -0.02346041055718475, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.03128054740957967, -0.03128054740957967, -0.03128054740957967, -0.02346041055718475, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9843597262952102, 0.9843597262952102, 0.9843597262952102, 0.9843597262952102, -0.03128054740957967, -1.0, -1.0, 0.0, 0.0, 0.0, -0.833822091886608, -1.0, -1.0, -0.739980449657869, -0.14076246334310852, -0.14076246334310852, -0.14076246334310852, -0.12512218963831867, -0.12512218963831867, -0.12512218963831867, -0.12512218963831867, -0.12512218963831867, -0.10948191593352884, -0.093841642228739, -0.093841642228739, 0.0, -0.07820136852394917, 0.0, -0.02346041055718475, -0.007820136852394917, 0.0, 0.9765395894428153, 0.9765395894428153, 0.9765395894428153, 0.9765395894428153, 0.42130987292277616, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997, 0.06158357771260997]), ("7, <class 'wpilib.cantalon.CANTalon'>", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])])

playback_macro = PlaybackMacro(shop_instructions, talon_arr)
#playback_macro = Pl

#Operation manager, controllers, and sensor pollers
operation_manager = OperationManager(shooter, pickup, straight_macro, record_macro, playback_macro)
override_manager = OverrideManager(shooter, pickup, compressor)

pickup_macro = PickupMacro(operation_manager, ball_switch=ball_switch)

ac = ArcadeDriveController(dt, driver_stick, shooter)
mc = MechController(driver_stick, xbox_controller, switch_panel, pickup, shooter, operation_manager, override_manager)


# Auto
basic_auto = BasicAuto(straight_macro)
cross_and_shoot_auto = CrossAndShootAuto(straight_macro, operation_manager)


# define DriverStation
ds = DriverStation.getInstance()

nt_ticker = NTTicker(shooter, pickup, straight_macro)

hid_sp = SensorPoller((driver_stick, xbox_controller, switch_panel, shooter.flywheel_sensor, shooter.turntable_sensor, shooter.hood_sensor, navx))
nt_sp = SensorPoller((nt_ticker,))






