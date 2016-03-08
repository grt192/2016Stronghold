"""
Config File for Robot
"""

from wpilib import Solenoid, Compressor, DriverStation, CANTalon, AnalogInput
import platform

from grt.sensors.attack_joystick import Attack3Joystick
from grt.sensors.xbox_joystick import XboxJoystick
from grt.sensors.switch_panel import SwitchPanel

from grt.sensors.navx import NavX
from grt.sensors.dummy import Mimic

from grt.core import SensorPoller

from grt.mechanism.drivetrain import DriveTrain
from grt.mechanism.drivecontroller import ArcadeDriveController
from grt.mechanism.mechcontroller import MechController
from grt.mechanism.pickup import Pickup
from grt.mechanism.shooter import Shooter
from grt.mechanism.operation_manager import OperationManager
from grt.mechanism.override_manager import OverrideManager
from grt.mechanism.motorset import Motorset
from grt.mechanism.rails import Rails
from grt.mechanism.flywheel import Flywheel
from grt.mechanism.turntable import TurnTable
from grt.mechanism.hood import Hood

from grt.vision.robot_vision import Vision

from grt.macro.straight_macro import StraightMacro
from grt.macro.record_macro import RecordMacro
from grt.macro.record_macro import PlaybackMacro

from grt.mechanism.nt_ticker import NTTicker
from grt.autonomous.one_cross_auto import OneCrossAuto
from collections import OrderedDict

using_vision_server = True

# Compressor initialization
compressor = Compressor()
compressor.start()

turntable_pot = AnalogInput(0)

# DT talons and objects
dt_right = CANTalon(1)
dt_left = CANTalon(11)
dt_shifter = Solenoid(0)

if "Linux" in platform.platform():
    dt_r2 = CANTalon(2)
    dt_r3 = CANTalon(3)

    dt_l2 = CANTalon(12)
    dt_l3 = CANTalon(13)

    Motorset.group((dt_right, dt_r2, dt_r3))
    Motorset.group((dt_left, dt_l2, dt_l3))

dt = DriveTrain(dt_left, dt_right, left_shifter=dt_shifter, left_encoder=None, right_encoder=None)

# Joysticks
driver_stick = Attack3Joystick(0)
xbox_controller = XboxJoystick(1)
switch_panel = SwitchPanel(2)

# Vision
robot_vision = Vision()
if using_vision_server:
    import grt.vision.vision_server
    grt.vision.vision_server.prepare_module(robot_vision)

# Flywheel
flywheel_motor = CANTalon(10)
flywheel_motor2 = CANTalon(4)
Motorset.group((flywheel_motor, flywheel_motor2))

flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
#flywheel_motor.setPID(.33, 0, 0, f=.19) #Omega 1 tuning constants
flywheel_motor.setPID(.33, 0, 0, f=.3) #Omega 2 tuning constants

flywheel = Flywheel(robot_vision, flywheel_motor)

# Rails
rails_actuator = Solenoid(1)
rails = Rails(rails_actuator)

# See about configuring a max output voltage

# Turntable
turntable_motor = CANTalon(5)
turntable_motor.setFeedbackDevice(CANTalon.FeedbackDevice.AnalogPot)
turntable_motor.setPID(90, 0, 0, f=0)
turntable_motor.configMaxOutputVoltage(8)
turntable_motor.setAllowableClosedLoopErr(2)
turntable_motor.reverseOutput(True)
turntable_motor.changeControlMode(CANTalon.ControlMode.Position)

turntable = TurnTable(robot_vision, turntable_motor, dt)

# Hood
hood_motor = CANTalon(6)
hood_motor.setFeedbackDevice(CANTalon.FeedbackDevice.AnalogPot)
hood_motor.setPID(10, 0, 0, f=0)
hood_motor.configMaxOutputVoltage(5)
hood_motor.setAllowableClosedLoopErr(5)
hood_motor.changeControlMode(CANTalon.ControlMode.Position)

hood = Hood(robot_vision, hood_motor)

shooter = Shooter(robot_vision, flywheel, turntable, hood, rails)

# Magic numbers for shooting:
# Raise the hood to 35 degrees (potentiometer position 247)
# Set the flywheel speed to 2600 ticks
# Check these numbers with the google spreadsheet
# Also see about adding in automatic alignment/chival de fris macro/ light-sensor-controlled pickup


# Pickup
pickup_achange_motor1 = CANTalon(8)
pickup_achange_motor2 = CANTalon(9)

pickup_roller_motor = CANTalon(7)

pickup_achange_motor1.changeControlMode(CANTalon.ControlMode.Position)
pickup_achange_motor1.setFeedbackDevice(CANTalon.FeedbackDevice.AnalogPot)
pickup_achange_motor1.setPID(20, 0, 0, f=0)
pickup_achange_motor1.setAllowableClosedLoopErr(5)
pickup_achange_motor2.changeControlMode(CANTalon.ControlMode.Position)
pickup_achange_motor2.setFeedbackDevice(CANTalon.FeedbackDevice.AnalogPot)
pickup_achange_motor2.setPID(20, 0, 0, f=0)
pickup_achange_motor2.setAllowableClosedLoopErr(5)

pickup = Pickup(pickup_achange_motor1, pickup_achange_motor2, pickup_roller_motor)

# Straight macro initialization
navx = NavX()
straight_macro = StraightMacro(dt, navx)
one_cross_auto = OneCrossAuto(straight_macro)

# Record macro initialization
talon_arr = [dt_left, dt_right, pickup_achange_motor1, pickup_achange_motor2, pickup_roller_motor]
record_macro = RecordMacro(talon_arr)
sim_instructions = OrderedDict([("11, <class 'wpilib.cantalon.CANTalon'>", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798]), ("1, <class 'wpilib.cantalon.CANTalon'>", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, -0.5659824046920822, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798, 0.24926686217008798]), ("8, <class 'wpilib.cantalon.CANTalon'>", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), ("9, <class 'wpilib.cantalon.CANTalon'>", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), ("7, <class 'wpilib.cantalon.CANTalon'>", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])])

playback_macro = PlaybackMacro(sim_instructions, talon_arr)
#playback_macro = Pl

#Operation manager, controllers, and sensor pollers
operation_manager = OperationManager(shooter, pickup, straight_macro, record_macro, playback_macro)
override_manager = OverrideManager(shooter, pickup, compressor)

ac = ArcadeDriveController(dt, driver_stick, shooter, straight_macro, operation_manager)
mc = MechController(driver_stick, xbox_controller, switch_panel, pickup, shooter, operation_manager, override_manager)

# define DriverStation
ds = DriverStation.getInstance()

nt_ticker = NTTicker(shooter, pickup, straight_macro)

hid_sp = SensorPoller((driver_stick, xbox_controller, switch_panel, shooter.flywheel_sensor, shooter.turntable_sensor, shooter.hood_sensor, navx))
nt_sp = SensorPoller((nt_ticker,))






