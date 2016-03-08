from wpilib import CANTalon
import threading
LEFT_PICKUP_DOWN_POSITION = 674
LEFT_PICKUP_UP_POSITION = LEFT_PICKUP_DOWN_POSITION - 130

RIGHT_PICKUP_DOWN_POSITION = 815
RIGHT_PICKUP_UP_POSITION = RIGHT_PICKUP_DOWN_POSITION + 115

LEFT_PICKUP_CROSS_POSITION = 640
RIGHT_PICKUP_CROSS_POSITION = 845

#Talon 9 (left motor, achange2) zero: 674
#Talon 8 (right motor, achange1) zero: 815
#Talon 8 frame: 945
#Talon 9 frame: 555

class Pickup:

    def __init__(self, achange_motor_1, achange_motor_2, roller_motor):
        self.operation_manager = None
        self.override_manager = None
        self.achange_motor_1 = achange_motor_1
        self.achange_motor_2 = achange_motor_2
        self.roller_motor = roller_motor
        self.disable_timer = threading.Timer(2.5, self.disable_automatic_control)
        self.current_position = "frame"

    def angle_change(self, power):
        if self.achange_motor_1.getControlMode() == CANTalon.ControlMode.PercentVbus  and self.achange_motor_2.getControlMode() == CANTalon.ControlMode.PercentVbus:
            self.achange_motor_1.set(power*.8)
            self.achange_motor_2.set(-power)

    def roll(self, power):
        self.roller_motor.set(-power*.7)
    def stop(self):
        self.roller_motor.set(0)


    def go_to_pickup_position(self):
        self.disable_timer.cancel()
        self.enable_automatic_control()
        self.current_position = "pickup"
        self.auto_set_left(LEFT_PICKUP_DOWN_POSITION)
        self.auto_set_right(RIGHT_PICKUP_DOWN_POSITION)
        self.disable_timer = threading.Timer(2.5, self.disable_automatic_control)
        self.disable_timer.start()

    def auto_set_left(self, angle):
        if not self.achange_motor_2.getControlMode() == CANTalon.ControlMode.PercentVbus:
            self.achange_motor_2.set(angle)
            #threading.Timer(2.5, self.disable_automatic_control)
            print("Auto-setting: ", angle)

    def auto_set_right(self, angle):
        if not self.achange_motor_1.getControlMode() == CANTalon.ControlMode.PercentVbus:
            self.achange_motor_1.set(angle)
            #threading.Timer(2.5, self.disable_automatic_control)


    def go_to_frame_position(self):
        self.disable_timer.cancel()
        self.enable_automatic_control()
        self.current_position = "frame"
        self.auto_set_left(LEFT_PICKUP_UP_POSITION)
        self.auto_set_right(RIGHT_PICKUP_UP_POSITION)
        self.disable_timer = threading.Timer(2.5, self.disable_automatic_control)
        self.disable_timer.start()

    def go_to_cross_position(self):
        self.enable_automatic_control()
        self.current_position = "cross"
        self.auto_set_left(LEFT_PICKUP_CROSS_POSITION)
        self.auto_set_right(RIGHT_PICKUP_CROSS_POSITION)

    def enable_automatic_control(self):
        if not self.override_manager.pickup_override:
            self.achange_motor_1.changeControlMode(CANTalon.ControlMode.Position)
            self.achange_motor_2.changeControlMode(CANTalon.ControlMode.Position)

    def disable_automatic_control(self):
        #print("Automatic control disabled!")
        self.achange_motor_1.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.achange_motor_2.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.achange_motor_1.set(0)
        self.achange_motor_2.set(0)



    #Pass this the actual flywheel class, eventually.