import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import os
import sys
from string import Template


#pops up a black and white video screen, note: is mirrored
#This creates a video object
cap = cv2.VideoCapture(0)

face_cascade_path = sys.argv[1]
face_cascade = cv2.CascadeClassifier(os.path.expanduser(face_cascade_path))

scale_factor = 1.1
min_neighbors = 3
min_size = (30, 30)
flags = cv2.cv.CV_HAAR_SCALE_IMAGE

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()#returns true/false frame is running correctly, shows error
    
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #line1 = cv2.line(gray,(0,0),(511,511),(255,0,0),5)

    #img = cv2.imread(gray, 0)
    # first argument is the haarcascades path
    
    faces = face_cascade.detectMultiScale(frame, scaleFactor = scale_factor, minNeighbors = min_neighbors,
        minSize = min_size, flags = flags)
        
    print(type(faces))
    #print(faces.shape)
    
    for( x, y, w, h ) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)

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
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()