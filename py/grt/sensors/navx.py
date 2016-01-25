from robotpy_ext.common_drivers.navx.ahrs import AHRS
from grt.core import Sensor


class NavX(Sensor):

	def __init__(self):
		
		super().__init__()

		self.ahrs = AHRS.create_spi()

		self.pitch = None
		self.yaw = None
		self.roll = None
		self.compass_heading = None
		self.fused_heading = None

	def poll(self):
		
		self.pitch = self.ahrs.getPitch()

		self.yaw = self.ahrs.getYaw()

		self.roll = self.ahrs.getRoll()

		self.compass_heading = self.ahrs.getCompassHeading()

		self.fused_heading = self.ahrs.getFusedHeading()