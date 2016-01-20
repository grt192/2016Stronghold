#execfile("../camscript.py")
import platform
if "Linux" in platform.platform():
    with open("/home/lvuser/py/grt/vision/camscript_new.py") as f:
        code = compile(f.read(), "/home/lvuser/py/grt/vision/camscript_new.py", 'exec')
        exec(code)



import wpilib
import time
import threading
#camera = wpilib.USBCamera()
#camera.startCapture()
#camera.setExposureAuto() #-1 old
#camera.setBrightness(20)
#camera.stopCapture()
#camera.setSize(camera.width / 2, camera.height / 2)
#camera.setFPS(15)
#cameraServer = wpilib.CameraServer()
#cameraServer.startAutomaticCapture(camera)

class MyRobot(wpilib.SampleRobot):
    def __init__(self):
        super().__init__()
        import config
      
        self.hid_sp = config.hid_sp
        self.ds = config.ds
        #self.vision = config.vision
        
        #self.vision = config.vision
        #self.vision_thread = threading.Thread(target=self.vision.vision_main)
        #self.vision_thread.start()
        #self.cv2 = config.cv2


    def disabled(self):
        while self.isDisabled():
            tinit = time.time()
           
            self.safeSleep(tinit, .04)
            #print(self.cv2.__version__)
    
    def autonomous(self):
        # define auto here
        pass
    
    def operatorControl(self):
        while self.isOperatorControl() and self.isEnabled():
            tinit = time.time()
           
            self.hid_sp.poll()
            self.safeSleep(tinit, .04)
            
    def safeSleep(self, tinit, duration):
        tdif = .04 - (time.time() - tinit)
        if tdif > 0:
            time.sleep(tdif)
        if tdif <= 0:
            print("Code running slowly!")


if __name__ == "__main__":
    wpilib.run(MyRobot)
