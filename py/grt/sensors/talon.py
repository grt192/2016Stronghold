from wpilib import CANTalon
from grt.core import Sensor


class GRTTalon:
    def __init__(self, channel):
        self.t = CANTalon(channel)
        self.channel = channel

    def set(self, power):
        self.t.set(power)

    def get(self):
        return self.t.get()

    def getDeviceID(self):
        return self.t.getDeviceID()

    def changeControlMode(self, mode):
        self.t.changeControlMode(mode)

    def setP(self, value):
        self.t.setP(value)

    def setI(self, value):
        self.t.setI(value)

    def setD(self, value):
        self.t.setD(value)

    def poll(self):
        # self.busVoltage = t.getBusVoltage()
        # self.closeLoopRampRate = t.getCloseLoopRampRate()
        self.controlMode = self.t.getControlMode()
        self.deviceID = self.t.getDeviceID()
        self.encPosition = self.t.getEncPosition()
        self.encVelocity = self.t.getEncVelocity()
        self.outputCurrent = self.t.getOutputCurrent()
        self.outputVoltage = self.t.getOutputVoltage()
        self.closeLoopError = self.t.getCloseLoopError()
        # self.position = t.getPosition()
        # self.sensorPosition = t.getSensorPosition()
        # self.sensorVelocity = t.getSensorVelocity()
        # self.speed = t.getSpeed()
        # self.temp = t.getTemp()
