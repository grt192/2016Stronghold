"""
Config File for Robot
"""

from wpilib import Solenoid, Compressor, DriverStation, CANTalon, AnalogInput

from grt.sensors.attack_joystick import Attack3Joystick
from grt.sensors.xbox_joystick import XboxJoystick
from grt.sensors.dummy import Mimic
from grt.sensors.navx import NavX
from grt.sensors.switch_panel import SwitchPanel

from grt.core import SensorPoller

from grt.mechanism.drivetrain import DriveTrain
from grt.mechanism.drivecontroller import ArcadeDriveController
from grt.mechanism.mechcontroller import MechController
from grt.mechanism.pickup import Pickup
from grt.mechanism.operation_manager import OperationManager
from grt.mechanism.override_manager import OverrideManager
from grt.mechanism.motorset import Motorset
from grt.mechanism.shooter import Shooter
from grt.mechanism.flywheel import Flywheel
from grt.mechanism.rails import Rails
from grt.mechanism.turntable import TurnTable
from grt.mechanism.hood import Hood

# from grt.vision.robot_vision import Vision
from grt.macro.straight_macro import StraightMacro
from grt.macro.record_macro import RecordMacro

# Magic numbers for shooting:
# Raise the hood to 35 degrees (potentiometer position 247)
# Set the flywheel speed to 2600 ticks
# Check these numbers with the google spreadsheet
# Also see about adding in automatic alignment/chival de fris macro/ light-sensor-controlled pickup


using_vision_server = False

# Compressor initialization
compressor = Compressor()
compressor.start()

turntable_pot = AnalogInput(0)

# DT talons and objects
dt_right = CANTalon(1)
# dt_r2 = CANTalon(2)
# dt_r3 = CANTalon(3)

dt_left = CANTalon(11)
# dt_l2 = CANTalon(12)
# dt_l3 = CANTalon(13)
dt_shifter = Solenoid(0)

# Motorset.group((dt_right, dt_r2, dt_r3))
# Motorset.group((dt_left, dt_l2, dt_l3))

dt = DriveTrain(dt_left, dt_right, left_shifter=dt_shifter, left_encoder=None, right_encoder=None)



# Vision
robot_vision = Mimic(target_view=False, rotational_error=0, vertical_error=0,
                     getLowerThreshold=lambda: [1, 1, 1],
                     getUpperThreshold=lambda: [2, 2, 2],
                     setThreshold=lambda x, y: x)

# robot_vision = Vision()
if using_vision_server:
    import grt.vision.vision_server
    grt.vision.vision_server.prepare_module(robot_vision)

# Shooter objects

# Flywheel motors
flywheel_motor = CANTalon(10)
flywheel_motor2 = CANTalon(4)

Motorset.group((flywheel_motor, flywheel_motor2))

flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
flywheel_motor.setPID(.33, 0, 0, f=.19)

flywheel = Flywheel(robot_vision, flywheel_motor)

# Rails
rails_actuator = Solenoid(1)
rails = Rails(rails_actuator)

# Turntable
# TODO: See about configuring a max output voltage
turntable_motor = CANTalon(5)
turntable_motor.setFeedbackDevice(CANTalon.FeedbackDevice.AnalogPot)
turntable_motor.setPID(.01, 0, 0, f=0)
turntable_motor.changeControlMode(CANTalon.ControlMode.Position)
turntable = TurnTable(robot_vision, turntable_motor, dt)

# Hood
hood_motor = CANTalon(6)
hood_motor.setFeedbackDevice(CANTalon.FeedbackDevice.AnalogPot)
hood_motor.setPID(.1, 0, 0, f=0)
hood_motor.changeControlMode(CANTalon.ControlMode.Position)

hood = Hood(robot_vision, hood_motor)


shooter = Shooter(robot_vision, flywheel, turntable, hood, rails)



# Pickup Talons and Objects
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

# Straight macro initialization
navx = NavX()
straight_macro = StraightMacro(dt, navx)

# Record macro initialization
talon_arr = [dt_left, dt_right, pickup_achange_motor1, pickup_achange_motor2, pickup_roller_motor]
record_macro = RecordMacro(talon_arr)

# Operation manager, controllers, and sensor pollers
operation_manager = OperationManager(shooter, pickup, straight_macro)
override_manager = OverrideManager(shooter, pickup, compressor)

# Human Interface Devices
driver_stick = Attack3Joystick(0)
xbox_controller = XboxJoystick(1)
switch_panel = SwitchPanel(2)
# mimic_joystick = Attack3Joystick(3)

hid_sp = SensorPoller((driver_stick, xbox_controller,
                       switch_panel, shooter.flywheel_sensor,
                       shooter.turntable_sensor,
                       shooter.hood_sensor, navx))

ac = ArcadeDriveController(dt, driver_stick, operation_manager)
mc = MechController(driver_stick, xbox_controller, switch_panel, pickup, shooter, operation_manager, override_manager)

# talon_log_arr = [dt_left, dt_l2, dt_l3, dt_right, dt_r2, dt_r3, flywheel_motor, flywheel_motor2, hood_motor,
#                  turntable_motor, pickup_achange_motor1, pickup_achange_motor2, pickup_roller_motor]
talon_log_arr = [dt_left, dt_right, flywheel_motor, flywheel_motor2, hood_motor,
                 turntable_motor, pickup_achange_motor1, pickup_achange_motor2, pickup_roller_motor]

# define DriverStation
ds = DriverStation.getInstance()
