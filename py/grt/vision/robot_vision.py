import cv2
import numpy as np
import time, math, threading
"""
Do not get properties within this class because you will be in danger of recursive lock aquisition.
"""

class Vision:
    # GREEN_LOWER = np.array([0, 100, 0], 'uint8')
    # GREEN_UPPER = np.array([200, 255, 100], 'uint8')
    # GREEN_LOWER_HSV = np.array([75, 100, 160], 'uint8') #Computer
    # GREEN_UPPER_HSV = np.array([130, 255, 255], 'uint8') #Computer

    GREEN_LOWER_HSV = np.array([75, 80, 100], 'uint8')
    GREEN_UPPER_HSV = np.array([130, 255, 255], 'uint8')
    drawing = True
    status_print = False

    POLY_ARC_LENGTH = .015
    POLY_MIN_SIDES = 6
    POLY_MAX_SIDES = 11

    MIN_AREA = 100

    DEFAULT_ERROR = 1000

    # Color Ranges:
    # Gimp: H = 0-360, S = 0-100, V = 0-100
    # OpenCV: H = 0-180, S = 0-255, V = 0-255

    def __init__(self):
        print("robotvision init")
        # self.vision_sensor = vision_sensor

        # Properties
        self._target_view = False
        self._rotational_error = self._vertical_error = self.DEFAULT_ERROR
        print("robot_vision constants")

        self.vision_lock = threading.Lock()
        self.threshold_lock = threading.Lock()
        print("making vision_thread")
        self.vision_thread = threading.Thread(target=self.vision_main)
        print("starting vision thread")
        self.vision_thread.start()

    def vision_init(self):
        self.cap = cv2.VideoCapture(0)
        _, self.img = self.cap.read()
        self.height, self.width, channels = self.img.shape
        self.x_target = int(self.width / 2)

    def vision_main(self):
        self.vision_init()
        while True:
            try:
                self.vision_loop()
            except KeyboardInterrupt:
                self.vision_close()
                break

    @property
    def target_view(self):
        print("getting target view: ")
        self._target_view = 1
        with self.vision_lock:
            self._target_view = 2
            print("vision_lock target view")
            return self._target_view

    @target_view.setter
    def target_view(self, value):
        # Call the vision sensor listeners
        self.vision_sensor.target_view = value
        self._target_view = value

    @property
    def rotational_error(self):
        print("Getting rotational Error")
        with self.vision_lock:
            return self._rotational_error

    @rotational_error.setter
    def rotational_error(self, value):
        # Call the vision sensor listeners
        self.vision_sensor.rotational_error = value
        self._rotational_error = value

    @property
    def vertical_error(self):
        with self.vision_lock:
            return self._vertical_error

    @vertical_error.setter
    def vertical_error(self, value):
        # Call the vision sensor listeners
        self.vision_sensor.rotational_error = value
        self._vertical_error = value

    def vision_close(self):
        cv2.destroyAllWindows()

    def get_max_polygon(self, img):
        # Get HSV Image
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Threshold Image
        thresh = cv2.inRange(hsv, self.GREEN_LOWER_HSV, self.GREEN_UPPER_HSV)

        # Get Contours
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Get Polygon Approximation list
        polygons = map(lambda curve: cv2.approxPolyDP(curve, self.POLY_ARC_LENGTH * cv2.arcLength(curve, closed=True),
                                                      closed=True), contours)

        # Filter Curves:
        polygons = filter(lambda poly: self.POLY_MIN_SIDES <= poly.shape[0] <= self.POLY_MAX_SIDES and
                                       cv2.contourArea(poly) > self.MIN_AREA, polygons)

        try:
            # Get Maximum-Area Polygon
            max_area_poly = max(polygons, key=cv2.contourArea)
            # print("Max Area Poly", )

            target_view = True
        except:
            target_view = False
            max_area_poly = None

        return target_view, max_area_poly

    def get_error(self, target):
        """ Get the rotational and vertical error of the camera
        :param target:
        :return: (rotational_error, vertical_error)
        """
        moments = cv2.moments(target)

        # Experimental - Actual
        rotational_error = int(moments['m10'] / moments['m00']) - self.x_target

        vertical_error = int(moments['m01'] / moments['m00'])

        return rotational_error, vertical_error

    def print_all_values(self):
        if self.status_print:
            # Initial distance calibration
            # distance = .0016 * (self.vertical_error ** 2) - .7107 * self.vertical_error + 162.09
            distance = .0021 * (self.vertical_error ** 2) - 1.2973 * self.vertical_error + 261.67
            print("Target View: ", self._target_view, "Rotational Error: ", self._rotational_error,
                  "Vertical Error: ", self._vertical_error, "Distance: ", distance, sep="     ")

    def get_frame(self):
        img_jpg = cv2.imencode(".jpg", self.img)
        print("Returning frame")
        return img_jpg

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
        # At the beginning of the loop, self.target_view is set to false
        # If something useful is found, self.target_view is set to true


        # print("Exposure: ", self.cap.get(cv2.CAP_PROP_FPS))

        _, img = self.cap.read()
        print("looping vision")
        target_view, max_polygon = self.get_max_polygon(img)

        with self.vision_lock:
            print("inside vision_lock _vision loop")
            # Update properties
            print("Setting target view")
            self.target_view = target_view
            print("Set target view")
            if self._target_view:
                print("Inside self.target_view")
                self.rotational_error, self.vertical_error = self.get_error(max_polygon)

            print("done with with statement")
            # Draw on image
            if self.drawing:
                cv2.drawContours(img, [max_polygon], -1, (255, 0, 0), 2)
            print("drawing done")

        print("outside with")
        self.img = img
        cv2.imshow("Image", self.img)
        self.print_all_values()
        cv2.waitKey(25)
        # time.sleep(.025)