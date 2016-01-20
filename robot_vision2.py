import cv2
import numpy as np
import time, math, threading

class Vision:
    GREEN_LOWER = np.array([0, 100, 0], 'uint8')
    GREEN_UPPER = np.array([200, 255, 100], 'uint8')
    # GREEN_LOWER_HSV = np.array([75, 100, 160], 'uint8') #Computer
    # GREEN_UPPER_HSV = np.array([130, 255, 255], 'uint8') #Computer

    GREEN_LOWER_HSV = np.array([75, 80, 100], 'uint8')
    GREEN_UPPER_HSV = np.array([130, 255, 255], 'uint8')
    cap = vector_mat = x_mat = y_mat = contour_amax = target_polygon = x_cm = y_cm = target_polygon_opened = rotational_error = height = width = contours = img = moments = avg_height = distance = None
    drawing = True
    should_abort = False
    status_print = True

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
        pass
        #self.vision_thread = threading.Thread(target=self.vision_main)
        #self.vision_thread.start()

    def vision_init(self):
        self.cap = cv2.VideoCapture(0)
        # self.wcam = wpilib.USBCamera()
        # self.wcam.startCapture()
        # self.wcam.setExposureAuto()
        # self.wcam.setExposureManual(10)
        self.vector_mat = np.ndarray((8, 3))
        self.x_mat = np.ndarray((4, 3))
        self.y_mat = np.ndarray((4, 3))
        _, self.img = self.cap.read()
        self.height, self.width, channels = self.img.shape
        self.x_target = int(self.width / 2)
        self.y_target = int(self.height / 2)
        self.allowed_error = 20


    def vision_close(self):
        cv2.destroyAllWindows()

    def get_contours(self):
        _, self.img = self.cap.read()
        #self.img = cv2.imread("img.bmp")
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        self.thresh = cv2.inRange(hsv, self.GREEN_LOWER_HSV, self.GREEN_UPPER_HSV)
        cv2.imshow("Thresh", self.thresh)
        #cv2.imwrite("/home/lvuser/py/thresh.bmp", thresh)

        im2, self.contours, hierarchy = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    def get_octagon(self):
        self.target_polygon = None  # Changed to get rid of the target polygon each cycle
        area_max = area = 0
        for c in self.contours:
            # print(c)
            poly = cv2.approxPolyDP(c, .015 * cv2.arcLength(c, True), True)
            if poly.shape[0] >= 6 and poly.shape[0] <= 11:
                # Shape is an octagon
                area = cv2.contourArea(poly)
                if area > area_max and area > 0:
                    area_max = area
                    self.target_polygon = poly
        if self.status_print:
            #pass
            print("Area: ", area_max)


    def get_rotational_error(self):
        moments = cv2.moments(self.target_polygon)
        self.x_cm = int(moments['m10'] / moments['m00'])
        self.y_cm = int(moments['m01'] / moments['m00'])
        self.rotational_error = self.x_cm - self.x_target  # Experimental - actual

    def draw_initial_parameters(self):
        cv2.circle(self.img, (self.x_cm, self.y_cm), 20, (255, 0, 0))
        cv2.circle(self.img, (self.x_target, self.y_target), 20, (0, 0, 255))
        cv2.drawContours(self.img, [self.target_polygon], -1, (255, 0, 0), 2)

    def get_polygon_matrix(self):
        self.target_polygon_opened = self.target_polygon[:, 0, :]
        # print(self.target_polygon_opened)

        # Form vectors from one point to the next (easier option?)
        i = j = k = 0
        try:
            for vector in self.vector_mat:
                if i < 7:
                    vector[0] = abs(self.target_polygon_opened[i, 0] - self.target_polygon_opened[i + 1, 0])
                    vector[1] = abs(self.target_polygon_opened[i, 1] - self.target_polygon_opened[i + 1, 1])

                if i == 7:
                    vector[0] = abs(self.target_polygon_opened[i, 0] - self.target_polygon_opened[0, 0])
                    vector[1] = abs(self.target_polygon_opened[i, 1] - self.target_polygon_opened[0, 1])
                i += 1

                vector[2] = math.sqrt(vector[0] ** 2 + vector[1] ** 2)

                if vector[1] > vector[0]:
                    if j == 4:
                        # The octagon is not formed properly --> abort
                        self.should_abort = True
                        break
                    self.y_mat[j] = vector
                    j += 1
                else:
                    if k == 4:
                        # The octagon is not formed properly --> abort
                        self.should_abort = True
                        break
                    self.x_mat[k] = vector
                    k += 1
        except IndexError:
            pass
            #self.should_abort = True
        finally:
            self.should_abort = False

    def get_avg_height(self):
        self.avg_height = np.mean(self.y_mat[:, 2])

    def get_distance(self):
        # distance = 5420.8 * (avg_height ** -.828)
        # horiz_dist = math.sqrt(abs((distance ** 2) - (41 ** 2)))
        # distance = -.6807*avg_height + 184.31
        # distance = -98.48 * math.log(avg_height) + 572.82
        self.distance = 275.56 * (math.e ** (-.008 * self.avg_height))

    def get_shooter_values(self):
        #GET ACTUAL DATA
        self.target_speed = self.distance
        self.target_angle = 45

    def print_all_values(self):
        if self.status_print:
            print("Rotational Error: ", self.rotational_error)
            #print("Average Height: ", self.avg_height)
            #print("Distance: ", self.distance)
            #print("Target Speed: ", self.target_speed)
            #print("Target Angle: ", self.target_angle)
    def get_frame(self):
        return self.img

    def vision_loop(self):
        # print("Exposure: ", self.cap.get(cv2.CAP_PROP_FPS))
        self.get_contours()
        self.get_octagon()

        if not self.target_polygon == None:
            # An octagon is visible

            self.get_polygon_matrix()
            self.get_rotational_error()
            if not self.should_abort:
                if self.drawing:
                    cv2.drawContours(self.img, [self.target_polygon], -1, (255, 0, 0), 2)
               
                if self.drawing:
                    self.draw_initial_parameters()

                self.get_avg_height()
                
                self.get_distance()

                self.get_shooter_values()
                self.print_all_values()
        cv2.imshow("Image", self.img)
        #_, img_jpg = cv2.imencode("jpg", self.img)
        #cv2.waitKey(0)   
        time.sleep(.025)
    def get_frame(self):
        _, img_jpg = cv2.imencode(".jpg", self.img)
        print("Getting frame")
        return img_jpg


from flask import Flask, render_template, Response

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.getFrame()
        time.sleep(.05)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

v = Vision()
def temp_func():
    app.run(host='0.0.0.0', debug=False, threaded=True)

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(v),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

t2 = threading.Thread(target=temp_func)
t2.start()
if __name__ == "__main__":
    #t = threading.Thread(target=v.vision_main)
    #t.start()
    
    v.vision_main()

    #v.vision_main()
        