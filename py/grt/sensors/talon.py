from wpilib import CANTalon
from grt.core import Sensor


class Talon:
    def __init__(self, channel):
        self.t = CANTalon(channel)
        self.channel = channel

    def set(self, power):
        self.t.set(power)

    def Get(self):
        return self.t.get()
        print(self.t.Get())

    def GetChannel(self):
        return self.channel

    def poll(self):
        self.busVoltage = self.t.getBusVoltage()
        self.closeLoopRampRate = self.t.getCloseLoopRampRate()
        self.controlMode = self.t.getControlMode()
        self.deviceID = self.t.getDeviceID()
        self.encPosition = self.t.getEncPosition()
        self.encVelocity = self.t.getEncVelocity()
        self.outputCurrent = self.t.getOutputCurrent()
        self.outputVoltage = self.t.getOutputVoltage()
        self.position = self.t.getPosition()
        self.sensorPosition = self.t.getSensorPosition()
        self.sensorVelocity = self.t.getSensorVelocity()
        self.speed = self.t.getSpeed()
        self.temp = self.t.getTemp()