# OpenCV program to access brightness levels in real time
# import libraries of python OpenCV
# where its functionality resides
import cv2
import time

# np is an alias pointing to numpy library
import numpy as np

# capture frames from a camera
cap = cv2.VideoCapture('videos/BrightnessTest.mp4')
#cap = cv2.VideoCapture(1)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH,2500);
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,2500);
#start_frame_number = 30
cap.set(cv2.CAP_PROP_FPS, 5)

# loop runs if capturing has been initialized
measurement = []
test = True
frame_rate = 10
frame_count = 0
vertical=True
while(test):

    #should be read by the stage
    frame_count = frame_count+1
    # reads frames from a camera
    ret, frame = cap.read()
    test = cap.isOpened()
    if not test:
        break
    if frame is None:
        test = False
        break

    frame_copy = frame.copy()

    gray = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2GRAY)
    meanGray = gray.mean()

    lab = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2LAB)
    L,A,B=cv2.split(lab)
    meanL = L.mean()

    hsv = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2HSV)
    H,S,V= cv2.split(hsv)
    meanH = H.mean()

    ## Debug text on screen
    cv2.putText(frame_copy, "{}: {:.2f}".format("GRY brightness ", meanGray), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv2.putText(frame_copy, "{}: {:.2f}".format("LAB brightness ", meanL), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv2.putText(frame_copy, "{}: {:.2f}".format("HSV brightness ", meanH), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.namedWindow('Original',cv2.WINDOW_NORMAL)
    cv2.imshow('Original',frame_copy)
    cv2.resizeWindow('Original', 1024,800)

    key = cv2.waitKey(1)
    if key == ('c'):
        break

# Close the window
cap.release()
# De-allocate any associated memory usage
cv2.destroyAllWindows()

