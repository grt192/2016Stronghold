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
		self.busVoltage = t.getBusVoltage()
		self.closeLoopRampRate = t.getCloseLoopRampRate()
		self.controlMode = t.getControlMode()
		self.deviceID = t.getDeviceID()
		self.encPosition = t.getEncPosition()
		self.encVelocity = t.getEncVelocity()
		self.outputCurrent = t.getOutputCurrent()
		self.outputVoltage = t.getOutputVoltage()
		self.position = t.getPosition()
		self.sensorPosition = t.getSensorPosition()
		self.sensorVelocity = t.getSensorVelocity()
		self.speed = t.getSpeed()
		self.temp = t.getTemp()