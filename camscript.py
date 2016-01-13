import wpilib

camera = wpilib.USBCamera()
camera.startCapture()
camera.setExposureAuto()
cameraServer = wpilib.CameraServer()
cameraServer.startAutomaticCapture(camera)
a = input()
