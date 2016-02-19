from wpilib import CANTalon


# TODO: Fix with properties and potentiometer readings.
class Pickup:
    def __init__(self, achange_motor1, achange_motor2, roller_motor):
        self.operation_manager = None

        self.achange_motor1 = achange_motor1
        self.achange_motor2 = achange_motor2
        self.roller_motor = roller_motor
        self.current_position = "frame"

    def angle_change(self, power):
        self.achange_motor1.set(power)
        self.achange_motor2.set(-power)

    def roll(self, power):
        self.roller_motor.set(power)

    def stop(self):
        self.roller_motor.set(0)

    def set_automatic(self):
        # self.achange_motor_1.changeControlMode(CANTalon.ControlMode.Position)
        self.achange_motor2.changeControlMode(CANTalon.ControlMode.Position)
        self.achange_motor2.setPID(5, 0, 0, 1)

    def set_manual(self):
        # self.achange_motor_1.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.achange_motor2.changeControlMode(CANTalon.ControlMode.PercentVbus)

    def zero(self):
        self.set_automatic()
        # self.achange_motor_1.setSensorPosition(0)
        self.achange_motor2.setSensorPosition(0)

    def go_to_zero(self):
        self.set_automatic()
        # self.achange_motor_1.set(0)
        self.current_position = "zero"
        self.achange_motor2.set(0)

    def go_to_frame(self):
        self.set_automatic()
        # self.achange_motor_1.set(2700)
        self.current_position = "frame"
        self.achange_motor2.set(300)

    def go_to_pickup_position(self):
    	self.set_automatic()
    	self.current_position = "pickup"
    	self.achange_motor2.set(0)

    def go_to_portcullis(self):
        self.set_automatic()
        # self.achange_motor_1.set(500)
        self.achange_motor2.set(100)
