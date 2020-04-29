# OpenCV program to perform Edge detection in real time
# import libraries of python OpenCV
# where its functionality resides
import cv2

# np is an alias pointing to numpy library
import numpy as np
from edge_finder import edge_find, rho_theta_to_xy, select_lines,average_over_nearby_lines,distance_between_lines
# capture frames from a camera
cap = cv2.VideoCapture('videos/focus.mp4')


# loop runs if capturing has been initialized
test = True
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
    
    cv2.namedWindow('Original',cv2.WINDOW_NORMAL)
    cv2.imshow('Original',frame) 
    cv2.resizeWindow('Original', 900,500)
    # Display edges in a frame
    xy_lines = []
    if lines is not None:
        for l in lines:
            for rho,theta in l:
                x1,y1,x2,y2 = rho_theta_to_xy(rho,theta)
                xy_lines.append((x1,y1,x2,y2))
    if xy_lines is not None:
        for l in xy_lines:
            cv2.line(line_copy,(l[0],l[1]),(l[2],l[3]),(0,0,255),2)
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
