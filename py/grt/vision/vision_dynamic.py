import cv2
import numpy as np
import time, math

src = np.array([[322, 388], [357, 728], [711, 396], [762, 708]], np.float32)
dst = np.array([[322, 388], [322, 728], [711, 388], [711, 728]], np.float32)
#Priority upper, priority left

transform = cv2.getPerspectiveTransform(src, dst)
print(transform)


GREEN_LOWER = np.array([0, 100, 0], 'uint8')
GREEN_UPPER = np.array([200, 255, 100], 'uint8')
GREEN_LOWER_HSV = np.array([75, 100, 160], 'uint8')
GREEN_UPPER_HSV = np.array([130, 255, 255], 'uint8')

#Gimp: H = 0-360, S = 0-100, V = 0-100
#OpenCV: H = 0-180, S = 0-255, V = 0-255

#Different depending on camera?

def main():
cap = cv2.VideoCapture(0)
vector_mat = np.ndarray((8, 8))
contour_amax = target_polygon = None

while True:
    _, img = cap.read()
    #img = cv2.imread("r2.jpg")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV", hsv)
    #Color space of robot camera could be RGB? (probably not)
    thresh = cv2.inRange(hsv, GREEN_LOWER_HSV, GREEN_UPPER_HSV)
    #print(thresh)
    cv2.imshow("Thresh", thresh)
    height, width, channels = img.shape
    #cv2.waitKey(0)

    #out_grey = out_img = thresh #cv2.warpPerspective(img, transform, (width, height))
    #print(img[0])
    #out_grey = cv2.cvtColor(out_img, cv2.COLOR_RGB2GRAY)

    #out_grey_cpy = np.array(out_grey)
    #im2, contours, hierarchy = cv2.findContours(out_grey,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(im2, contours, -1, (0,255,0), 3)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #poly = cv2.approxPolyDP(contours, 5.0, True)




    #cv2.drawContours(img, contours, -1, (0, 0, 255), 2)





    #cv2.drawContours(img, poly, -1, (255, 0, 0), 2)

    #edged = cv2.Canny(thresh, 30, 200)
    #cv2.imshow("Edged", edged)
    #cv2.drawContours(img, edged, 0, (0, 0, 255), 2)


    #Change this to select for octagons, and then for area (because of possible interference caused by the tower LEDs)
    #Also use our own LED strips to check for interference caused by arena lighting


    area_max = area = 0
    for c in contours:
        #print(c)
        poly = cv2.approxPolyDP(c, .008*cv2.arcLength(c, True), True)
        area = cv2.contourArea(poly)
        if area > area_max:
            area_max = area
            target_polygon = poly
    if target_polygon == None:
        pass
    #print("No target visible")
    else:
        cv2.drawContours(img, [target_polygon], -1, (255, 0, 0), 2)
        #print(target_polygon)
        target_polygon_opened = target_polygon[:, 0, :]
        #print(target_polygon_opened)

        #Form vectors from one point to the next (easier option?)
        #v01 = [abs(target_polygon[0, 0] - target_polygon[1, 0]), abs(target_polygon[0, 1] - target_polygon[1, 1])
        i = 0
        try:
            for vector in vector_mat:
                #print(vector)
                #print("I: ", i)
                #print(abs(target_polygon_opened[i, 0] - target_polygon_opened[i+1, 0]))
                #print(target_polygon_opened[i, 0])
                if i < 7:
                    vector[0] = abs(target_polygon_opened[i, 0] - target_polygon_opened[i+1, 0])
                    vector[1] = abs(target_polygon_opened[i, 1] - target_polygon_opened[i+1, 1])
                    vector[4] = target_polygon_opened[i, 0]
                    vector[5] = target_polygon_opened[i, 1]
                    vector[6] = target_polygon_opened[i+1, 0]
                    vector[7] = target_polygon_opened[i+1, 1]

                if i == 7:
                    vector[0] = abs(target_polygon_opened[i, 0] - target_polygon_opened[0, 0])
                    vector[1] = abs(target_polygon_opened[i, 1] - target_polygon_opened[0, 1])
                i += 1
        except IndexError:
            pass
        #print(vector_mat)
        for vector in vector_mat:
            if vector[1] > vector[0]: #y > x
                vector[2] = 1
            else:
                vector[2] = 0
            vector[3] = math.sqrt(vector[0] ** 2 + vector[1] ** 2)

        #print(vector_mat)
        #Index 0 is X position, index 1 is y position, index 2 is orientation (1 for y, 0 for x), index 3 is magnitude
        #Indecies 4-7 were just added
        #Index 4 is point 0x, 5 is 0y, 6 is 1x, 7 is 1y
        #Try to merge these for loops together, if possible, to potentially save compuational time
        x_mat = np.ndarray((4, 8))
        y_mat = np.ndarray((4, 8))
        i = j = 0
        try:
            for vector in vector_mat:
                if vector[2] == 1:
                    y_mat[i] = vector
                    i += 1
                else:
                    x_mat[j] = vector
                    j += 1
        except IndexError:
            pass
        #print("Rectangle oriented badly!")

        #print(x_mat)
        #print(y_mat)
        avg_height = np.mean(y_mat[:, 3])
        print(avg_height, ",")
    #for vector in y_mat:
    #	print(vector[3])



    #cv2.drawContours(img, poly, -1, (255, 0, 0), 2)
    #if cv2.contourArea(c) >= 20:
    #	poly = cv2.approxPolyDP(c, 50.0, True)
    #	cv2.drawContours(img, poly, 0, (0, 0, 255), 2)
    a = [1,2]
    for i in a:
        pass
        """
        area = cv2.contourArea(c)
        if area > area_max and area > 5:
            area_max = area
            contour_amax = c
        """
        """
    if not contour_amax == None:
        rect = cv2.minAreaRect(contour_amax)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        #print(box)
        #cv2.drawContours(thresh, [box], 0, (0, 0, 255), 2)
        poly = cv2.approxPolyDP(contour_amax, 5.0, True)
        cv2.drawContours(img, poly, 0, (0, 0, 255), 2)
        #cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
        """
        """
        line_0_x = box[0,0] - box[1,0]
        line_0_y = box[0,1] - box[1,1]
        if line_0_y > line_0_x: # line 0 to 1 is vertical
            vert_line = np.sqrt(((box[0,0] - box[1,0]) ** 2) + ((box[0,1] - box[1,1]) ** 2))
            hor_line = np.sqrt(((box[1,0] - box[2,0]) ** 2) + ((box[1,1] - box[2,1]) ** 2))
        else: # line 0 to 1 is horizontal
            vert_line = np.sqrt(((box[1,0] - box[2,0]) ** 2) + ((box[1,1] - box[2,1]) ** 2))
            hor_line = np.sqrt(((box[0,0] - box[1,0]) ** 2) + ((box[0,1] - box[1,1]) ** 2))

        print("\nHeight: ", vert_line)
        print("Width: ", hor_line)
        """
    else:
        pass
    #print("No contours")

    #cv2.drawContours(out_img, c, -1, (255, 0, 0), 3)
    #cv2.drawContours(out_img, cv2.convexHull(c), -1, (0, 255, 0), 3)
    cv2.imshow("Original", img)
    #cv2.imshow("Thresh", thresh)


    #edged = cv2.Canny(out_grey, 30, 200)
    cv2.waitKey(25)
cv2.destroyAllWindows()
#time.sleep(0.1)