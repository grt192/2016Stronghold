__author__ = 'Chela and Rose'

class Challoopa:
    def __init__(self, challoopa_motor1, challoopa_motor2, roller_motor):
        self.challoopa_motor1 = challoopa_motor1
        self.challoopa_motor2 = challoopa_motor2
        self.roller_motor = roller_motor

    def extend(self,power):
        self.challoopa_motor1.set(power)
        self.challoopa_motor2.set(power)

    def back(self):
        self.challoopa_motor1.set(-1)
        self.challoopa_motor2.set(-1)

    def spin_forward(self):
        self.roller_motor.set(1)

    def spin_backwards(self):
        self.roller_motor.set(-1)


