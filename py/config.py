"""
Config File for Robot
"""

from wpilib import Solenoid, Compressor, DriverStation, CANTalon

from grt.core import SensorPoller
from grt.macro.straight_macro import StraightMacro

from grt.sensors.attack_joystick import Attack3Joystick
from grt.sensors.xbox_joystick import XboxJoystick
from grt.sensors.navx import NavX
from grt.sensors.vision_sensor import VisionSensor
from grt.sensors.dummy import Mimic

from grt.mechanism.drivetrain import DriveTrain
from grt.mechanism.drivecontroller import ArcadeDriveController
from grt.mechanism.mechcontroller import MechController
from grt.mechanism.pickup import Pickup
from grt.mechanism.flywheel import Flywheel
from grt.mechanism.rails import Rails
from grt.mechanism.turntable import TurnTable
from grt.mechanism.hood import Hood
from grt.mechanism.motorset import Motorset
from grt.vision.robot_vision import Vision
from grt.mechanism.shooter import Shooter
from grt.mechanism.operation_manager import OperationManager
from grt.sensors.switch_panel import SwitchPanel
from grt.macro.record_macro import RecordMacro


using_vision_server = True


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



Motorset.group((dt_right, dt_r2))
Motorset.group((dt_left, dt_l2))


dt = DriveTrain(dt_left, dt_right, left_shifter=dt_shifter, left_encoder=None, right_encoder=None)


# Vision
vision_sensor = VisionSensor()
# robot_vision = Mimic(target_view=False, rotational_error=0, vertical_error=0)
robot_vision = Vision(vision_sensor)
if using_vision_server:
    import grt.vision.vision_server
    grt.vision.vision_server.prepare_module(robot_vision)

# Manual Pickup

pickup_angle_change_motor1 = CANTalon(11)
pickup_angle_change_motor2 = CANTalon(7)
pickup_roller_motor = CANTalon(8)
pickup = Pickup(pickup_angle_change_motor1, pickup_angle_change_motor2, pickup_roller_motor)

# Manual shooter Talons and Objects

rails_actuator = Solenoid(1)
flywheel_motor = CANTalon(10)
turntable_motor = CANTalon(12)
hood_motor = CANTalon(9)

flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
flywheel_motor.setP(.26)
flywheel_motor.setF(.29)


turntable = TurnTable(robot_vision, turntable_motor, dt)
rails = Rails(rails_actuator)
flywheel = Flywheel(robot_vision, flywheel_motor)
hood = Hood(robot_vision, hood_motor)


shooter = Shooter(robot_vision, vision_sensor, flywheel, turntable, hood, rails, vision_enabled=False)

# Gyro/Accelerometer NavX Board
navx = NavX()

# Straight macro initialization
straight_macro = StraightMacro(dt, navx)

#Record macro initialization
talon_arr = [dt_left, dt_right, pickup_angle_change_motor1, pickup_angle_change_motor2, pickup_roller_motor]
record_macro = RecordMacro(talon_arr)

# Drive Controllers and sensor pollers
driver_stick = Attack3Joystick(0)
xbox_controller = XboxJoystick(1)
switch_panel = SwitchPanel(2)

operation_manager = OperationManager(shooter, pickup, straight_macro)
ac = ArcadeDriveController(dt, driver_stick, operation_manager)

hid_sp = SensorPoller((driver_stick, vision_sensor, xbox_controller, switch_panel, navx))


# define MechController

mc = MechController(driver_stick, xbox_controller, switch_panel, shooter, pickup, operation_manager, robot_vision)

# define DriverStation
ds = DriverStation.getInstance()
