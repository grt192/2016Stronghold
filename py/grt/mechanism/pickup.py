class Pickup:
    def __init__(self, achange_motor_1, achange_motor_2, roller_motor):
        self.achange_motor_1 = achange_motor_1
        self.achange_motor_2 = achange_motor_2
        self.roller_motor = roller_motor

    def angle_change(self, power):
        self.achange_motor_1.set(power)
        self.achange_motor_2.set(-power)

    def roll(self, power):
        self.roller_motor.set(power)

    def stop(self):
        self.roller_motor.set(0)
