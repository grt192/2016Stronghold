import cv2
import numpy as np
import time, math, threading

import os
import sys
from string import Template

class Vision:

    #'uint8' -> data type for 8 bit unsigned(positive) numbers
    #defines 2 colors -> green lower and upper(rgb)
    GREEN_LOWER = np.array([0, 100, 0], 'uint8')
    GREEN_UPPER = np.array([200, 255, 100], 'uint8')
    # GREEN_LOWER_HSV = np.array([75, 100, 160], 'uint8') #Computer
    # GREEN_UPPER_HSV = np.array([130, 255, 255], 'uint8') #Computer


    #defines 2 colors in hsv(hue, saturation, value)
    GREEN_LOWER_HSV = np.array([75, 80, 100], 'uint8')
    GREEN_UPPER_HSV = np.array([130, 255, 255], 'uint8')
    drawing = True
    status_print = True

    POLY_ARC_LENGTH = .015
    POLY_MIN_SIDES = 6
    POLY_MAX_SIDES = 11

    MIN_AREA = 100

    DEFAULT_ERROR = 1000

    # Gimp: H = 0-360, S = 0-100, V = 0-100
    # OpenCV: H = 0-180, S = 0-255, V = 0-255
    def vision_main(self):
        #initializes stuff
        #self.vision_init()
        face_cascade_path = 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(os.path.expanduser(face_cascade_path))

        #loop forever until you hit a key
        while True:
            try:
                #self.vision_loop()
                self.face_tracking_loop()
            except KeyboardInterrupt:
                self.vision_close()
                break

    def __init__(self):
        self.target_view = False
        self.rotational_error = self.vertical_error = self.DEFAULT_ERROR
        self.vision_lock = threading.Lock()
        self.vision_thread = threading.Thread(target=self.vision_main)
        self.vision_thread.start()

    def vision_init(self):
        #cap = video capture object that lets you capture video
        self.cap = cv2.VideoCapture(0)
        #read functions returns 2 things, first thing gets ignored(_), second thing goes into img
        _, self.img = self.cap.read()
        #method: shape returns height, width, channels?
        self.height, self.width, channels = self.img.shape
        self.x_target = int(self.width / 2)



    def vision_close(self):
        cv2.destroyAllWindows()

    def get_max_contour(self, img):  #this is not used
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, self.GREEN_LOWER_HSV, self.GREEN_UPPER_HSV)
        #first one is source image, second is contour retrieval mode, third is contour approximation method
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        area_max = area = 0
        max_contour = None
        #for each contours: an array of arrays
        for c in contours:
            area = cv2.contourArea(c)
            #finds the largest contour area to get rid of spurious contours
            if area > area_max and area > self.MIN_AREA:
                area_max = area
                max_contour = c
        if max_contour == None:
            target_view = False
        else:
            target_view = True
        return (target_view, max_contour)

    def get_max_polygon(self, img):
        #takes image in rgb and convert it to hsv, and call it hsv
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #any color outside upper and lower values gets pulled out(hsv described in cylindrical coordinates)
        thresh = cv2.inRange(hsv, self.GREEN_LOWER_HSV, self.GREEN_UPPER_HSV)
        #takes thresholded image and finds contours
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        area_max = area = 0
        max_poly = None
        #for each contour
        for c in contours:
            #tries to make a simpler contour with fewer points
            poly = cv2.approxPolyDP(c, self.POLY_ARC_LENGTH * cv2.arcLength(c, True), True)
            #only looks at polygons with sides 6-11
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
            print("Target View: ", self.target_view, "   Rotational Error: ", self.rotational_error, "    Vertical Error: ", self.vertical_error, "     Distance: ", distance)
            #print("Vertical Error: ", self.vertical_error)
            #print("Rotational Error: ", self.rotational_error)
            #print("Rotational Error: ", self.rotational_error)
            #print("Average Height: ", self.avg_height)
            #print("Distance: ", self.distance)
            #print("Target Speed: ", self.target_speed)
            #print("Target Angle: ", self.target_angle)
    def getFrame(self):
        img_jpg = cv2.imencode(".jpg", self.img)
        print("Returning frame")
        return img_jpg

    def getTargetView(self):
        with self.vision_lock:
            return self.target_view
    def getRotationalError(self):
        with self.vision_lock:
            return self.rotational_error

    def getTargetAngle(self):
        with self.vision_lock:
            return self.vertical_error * 1 #Fancy conversion equation here

    def getTargetSpeed(self):
        with self.vision_lock:
            return self.vertical_error * 1 #Fancy coversion equation here

    def get_face(self, img):

        scale_factor = 1.1
        min_neighbors = 3
        min_size = (30, 30)
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE

        faces = self.face_cascade.detectMultiScale(img, scaleFactor = scale_factor, minNeighbors = min_neighbors,
                                                   minSize = min_size, flags = flags)


        mf = 0
        mx = 0
        my = 0
        mw = 0
        mh = 0
        for (x, y, w, h) in faces:

            aof = w * h
            if(aof > mf):
                mf = aof
            mx = x
            my = y
            mw = w
            mh = h

    cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    return target_view, x, y, w, h


def vision_loop(self):
    #At the beginning of the loop, self.target_view is set to false
    #If something useful is found, self.target_view is set to true
    target_view = False
    # print("Exposure: ", self.cap.get(cv2.CAP_PROP_FPS))
    #captures frame every time loop is run
    _, img = self.cap.read()
    #gets if the target is detected, and the array of the polygon that fits constraints
    target_view, max_polygon = self.get_max_polygon(img)
    #?
    #with makes sure the vision gets unlocked after
    #threads -> so 2 things can run seperatly
    #vision system must be locked before self.target_view can be modified -> are shared with othet threads?
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

def face_tracking_loop(self):
    #At the beginning of the loop, target_view is set to false
    #If something useful is found, target_view is set to true
    target_view = False
    # print("Exposure: ", self.cap.get(cv2.CAP_PROP_FPS))
    #captures frame every time loop is run
    _, img = self.cap.read()
    #gets if the target is detected, and the array of the polygon that fits constraints
    target_view, x, y, w, h = self.get_face(img)
    #?
    #with makes sure the vision gets unlocked after
    #threads -> so 2 things can run seperatly
    #vision system must be locked before self.target_view can be modified -> are shared with othet threads?
    with self.vision_lock:
        self.target_view = target_view
        if target_view and self.drawing:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
        self.img = img
        if self.target_view:
            #self.rotational_error, self.vertical_error = self.get_error(max_polygon)
            #self.vertical_error = self.get_vertical_error(max_polygon)
            print("shoot")
        self.print_all_values()

    time.sleep(.025)
