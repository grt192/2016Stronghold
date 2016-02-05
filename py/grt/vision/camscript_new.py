import wpilib
import time

camera = wpilib.USBCamera()
camera.startCapture()
camera.setExposureAuto() #-1 old
camera.setBrightness(10)
#camera.setSize(camera.width / 2, camera.height / 2)
#camera.setFPS(15)
cameraServer = wpilib.CameraServer()
cameraServer.startAutomaticCapture(camera)
#a = input()
time.sleep(3)
camera.stopCapture()
