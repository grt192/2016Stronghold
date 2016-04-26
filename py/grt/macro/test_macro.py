import wpilib
import threading

class TestMacro:

    def __init__(self, motor1, motor2):

        self.motor1 = 0
        self.motor2 = 0

    def turn_left(self):
        count = 0
        self.motor1 = self.motor1 + 1
        print(self.motor1)
        return self.motor1

    def turn_right(self):
        self.motor2 = self.motor2 +1
        print(self.motor2)
        return self.motor2







