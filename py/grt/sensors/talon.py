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
        print(self.t.Get())

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
        self.controlMode = t.getControlMode()
        self.deviceID = t.getDeviceID()
        self.encPosition = t.getEncPosition()
        self.encVelocity = t.getEncVelocity()
        self.outputCurrent = t.getOutputCurrent()
        self.outputVoltage = t.getOutputVoltage()
        self.closeLoopError = t.getCloseLoopError()
        # self.position = t.getPosition()
        # self.sensorPosition = t.getSensorPosition()
        # self.sensorVelocity = t.getSensorVelocity()
        # self.speed = t.getSpeed()
        # self.temp = t.getTemp()
