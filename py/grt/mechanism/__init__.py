class Flywheel:
    def __init__(self, motor):
        self.motor = motor
        self.power = 0
        self.motor.set(self.power)

    def increment(self):
        if self.power >= -.9:
            self.power -= .01
            self.motor.set(self.power * 10)
            print("Power: ", self.power)

    def decrement(self):
        if self.power <= -.01:
            self.power += .01
            self.motor.set(self.power * 10)
            print("Power: ", self.power)
