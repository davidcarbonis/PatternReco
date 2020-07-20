# OpenCV program to perform Edge detection in real time
# import libraries of python OpenCV
# where its functionality resides
import cv2
import time

# np is an alias pointing to numpy library
import numpy as np
from edge_finder import edge_find, rho_theta_to_xy, select_lines,average_over_nearby_lines,distance_between_lines,find_intersections
# capture frames from a camera
cap = cv2.VideoCapture('videos/focus.mp4')


# loop runs if capturing has been initialized
test = True

singleCornerCounter = 0

while(test):

    #should be read by the stage
     
    # reads frames from a camera
    ret, frame = cap.read()
    test = cap.isOpened()
    if not test:
        break
    if frame is None:
        test = False
        break
    # Display an original image
    line_copy = frame.copy()
    # finds edges,countours, and hough lines in the input image image
    edges,cnts,lines = edge_find(frame)

    threshold = 0.1
    xy = find_intersections(lines, threshold)
    
    cv2.namedWindow('Original',cv2.WINDOW_NORMAL)
    cv2.imshow('Original',frame) 
    cv2.resizeWindow('Original', 900,500)

    # Display edges in a frame
    if lines is not None:
        for l in lines:
            cv2.line(line_copy,(l.x1,l.y1),(l.x2,l.y2),(0,0,255),2,cv2.LINE_AA)

    if xy is not None:
        for corner in xy:
            cv2.circle(line_copy, tuple(corner), 25, (0,255,0), 5)
    if (len(xy) == 1) : singleCornerCounter += 1
    elif (len(xy) != 1) : singleCornerCounter = 0
    if (singleCornerCounter == 5) : time.sleep(10)

    cv2.namedWindow('Edges',cv2.WINDOW_NORMAL)    
    cv2.imshow('Edges',line_copy)
    cv2.resizeWindow('Edges', 900,500)
    key = cv2.waitKey(1) 
    if key == ('c'):
        break

# Close the window
cap.release()
# De-allocate any associated memory usage
cv2.destroyAllWindows()

