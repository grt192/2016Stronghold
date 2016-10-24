import cv2
import numpy as np
import time, math, threading

class Vision:
    #GREEN_LOWER = np.array([0, 100, 0], 'uint8')   #Computer
    #GREEN_UPPER = np.array([200, 255, 100], 'uint8')    #Computer
    #GREEN_LOWER_HSV = np.array([75, 100, 160], 'uint8') #Computer
    #GREEN_UPPER_HSV = np.array([130, 255, 255], 'uint8') #Computer

    #GREEN_LOWER_HSV = np.array([75, 80, 100], 'uint8')  #Original Arizona arrival
    #GREEN_UPPER_HSV = np.array([130, 255, 255], 'uint8') #Original Arizona arrival
    #GREEN_LOWER_HSV = np.array([0, 0, 80], 'uint8') #Daylight
    #GREEN_UPPER_HSV = np.array([130, 150, 150], 'uint8') #Daylight

    # GREEN_LOWER_HSV = np.array([60, 60, 60], 'uint8')
    # GREEN_UPPER_HSV = np.array([170, 255, 220], 'uint8')

    GREEN_LOWER_HSV = np.array([50, 50, 50], 'uint8')
    GREEN_UPPER_HSV = np.array([170, 255, 220], 'uint8')
    

    drawing = True
    status_print = False

    POLY_ARC_LENGTH = .015
    POLY_MIN_SIDES = 6
    POLY_MAX_SIDES = 11

    MIN_AREA = 100

    DEFAULT_ERROR = 1000

    # Gimp: H = 0-360, S = 0-100, V = 0-100
    # OpenCV: H = 0-180, S = 0-255, V = 0-255
    def vision_main(self):
        self.vision_init()
        while True:
            try:
                self.vision_loop()
            except KeyboardInterrupt:
                self.vision_close()
                break

    def __init__(self):
        self.target_view = False
        self.rotational_error = self.vertical_error = self.DEFAULT_ERROR
        self.vision_lock = threading.Lock()
        self.threshold_lock = threading.Lock()
        self.vision_thread = threading.Thread(target=self.vision_main)
        self.vision_thread.start()

    def vision_init(self):
        self.cap = cv2.VideoCapture(0)
        _, self.img = self.cap.read()
        self.height, self.width, channels = self.img.shape
        self.x_target = int(self.width / 2)


    def vision_close(self):
        cv2.destroyAllWindows()

    def get_max_contour(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        with self.threshold_lock:
            thresh = cv2.inRange(hsv, self.GREEN_LOWER_HSV, self.GREEN_UPPER_HSV)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        area_max = area = 0
        max_contour = None
        for c in contours:
            area = cv2.contourArea(c)
            if area > area_max and area > self.MIN_AREA:
                area_max = area
                max_contour = c
        if max_contour == None:
            target_view = False
        else:
            target_view = True
        return (target_view, max_contour)

    def get_max_polygon(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, self.GREEN_LOWER_HSV, self.GREEN_UPPER_HSV)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        area_max = area = 0
        max_poly = None
        for c in contours:
            poly = cv2.approxPolyDP(c, self.POLY_ARC_LENGTH * cv2.arcLength(c, True), True)
            if poly.shape[0] >= self.POLY_MIN_SIDES and poly.shape[0] <= self.POLY_MAX_SIDES:
                area = cv2.contourArea(poly)
                if area > area_max and area > self.MIN_AREA:
                    area_max = area
                    max_poly = poly
        if max_poly == None:
            target_view = False
        else:
            target_view = True
        return (target_view, max_poly)


    def get_error(self, target):
        moments = cv2.moments(target)
        x_cm = int(moments['m10'] / moments['m00'])
        vertical_error = y_cm = int(moments['m01'] / moments['m00'])
        rotational_error = x_cm - self.x_target  # Experimental - actual
        return (rotational_error, vertical_error)

    

    def print_all_values(self):
        if self.status_print:
            #Initial distance calibration
            #distance = .0016 * (self.vertical_error ** 2) - .7107 * self.vertical_error + 162.09
            distance = .0021 * (self.vertical_error ** 2) - 1.2973 * self.vertical_error + 261.67
            #print("Target View: ", self.target_view, "   Rotational Error: ", self.rotational_error, "    Vertical Error: ", self.vertical_error, "     Distance: ", distance)
            #print("Vertical Error: ", self.vertical_error)
            #print("Rotational Error: ", self.rotational_error)
            #print("Rotational Error: ", self.rotational_error)
            #print("Average Height: ", self.avg_height)
            #print("Distance: ", self.distance)
            #print("Target Speed: ", self.target_speed)
            #print("Target Angle: ", self.target_angle)
    def getFrame(self):
        img_jpg = cv2.imencode(".jpg", self.img, (cv2.IMWRITE_JPEG_QUALITY, 20))

        return img_jpg

    def getTargetView(self):
        with self.vision_lock:
            return self.target_view
    def getRotationalError(self):
        with self.vision_lock:
            return self.rotational_error

    def getVerticalError(self):
        with self.vision_lock:
            return self.vertical_error

    def getTargetAngle(self):
        with self.vision_lock:
            return self.vertical_error * 1 #Fancy conversion equation here

    def getTargetSpeed(self):
        with self.vision_lock:
            return self.vertical_error * 1 #Fancy coversion equation here

    def setThreshold(self, lower_threshold, upper_threshold):
        with self.threshold_lock:
            self.GREEN_LOWER_HSV = lower_threshold
            self.GREEN_UPPER_HSV = upper_threshold

    def getLowerThreshold(self):
        with self.threshold_lock:
            return self.GREEN_LOWER_HSV

    def getUpperThreshold(self):
        with self.threshold_lock:
            return self.GREEN_UPPER_HSV




    def vision_loop(self):
        #At the beginning of the loop, self.target_view is set to false
        #If something useful is found, self.target_view is set to true
        target_view = False
        # print("Exposure: ", self.cap.get(cv2.CAP_PROP_FPS))
        _, img = self.cap.read()
        target_view, max_polygon = self.get_max_polygon(img)
        with self.vision_lock:
            self.target_view = target_view
            if self.drawing:
                cv2.drawContours(img, [max_polygon], -1, (255, 0, 0), 2)
            self.img = img
            if self.target_view:
                self.rotational_error, self.vertical_error = self.get_error(max_polygon)
                #self.vertical_error = self.get_vertical_error(max_polygon)
            self.print_all_values()
               
        time.sleep(.025)
        