import wpilib
import time
try:
	camera = wpilib.USBCamera(name=b"cam1")
	camera.startCapture()
	camera.setExposureAuto() #-1 old
	camera.setExposureManual(-1)
	camera.setBrightness(100)
	#camera.setSize(camera.width / 2, camera.height / 2)
	#camera.setFPS(15)
	cameraServer = wpilib.CameraServer()
	cameraServer.startAutomaticCapture(camera)
	#a = input()
	time.sleep(3)
	camera.stopCapture()
except:
	pass
