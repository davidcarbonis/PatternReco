# OpenCV program to perform Edge detection in real time
# import libraries of python OpenCV
# where its functionality resides
import cv2
import time

# np is an alias pointing to numpy library
import numpy as np
from edge_finder import edge_find, rho_theta_to_xy, select_lines,average_over_nearby_lines,distance_between_lines,find_intersections, preprocess_image, floodfill_mask_image, cv2HoughLines

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
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges,cnts,lines = edge_find(grey_frame)


### Find HoughLines from a masked image
    ## post-flooodfill and masking canny parameters
    postMaskCannyThreshold1 = 15
    postMaskCannyThreshold2 = 50
    postMaskCannyAperture = 3
    
    ## floodfill and mask preprocessed image and edge detector said image
    h, w = edges.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(edges, mask, (0,0), 123);
    floodfill = edges.copy() 
    ## Apply masking
    bg = np.zeros_like(floodfill)
    bg[floodfill == 123] = 255
    bg = cv2.blur(bg, (1,1))
    masked_edges = cv2.Canny(bg, postMaskCannyThreshold1, postMaskCannyThreshold2, postMaskCannyAperture)

    ## find hough lines
    min_line_length = 0  # Original test value of 50
    max_line_gap = 0     # Original value of 20
    HTthreshold = 100      # Original value of 100
    probabilisticHT = False
    HTlines = cv2HoughLines(masked_edges, HTthreshold, min_line_length, max_line_gap, probabilisticHT)

    ## calculate variance of the lapacian to determine focus/blur
    laplacianVar = cv2.Laplacian(frame, cv2.CV_64F).var() ##apply laplacian to greyscale image
##    laplacianVar = cv2.Laplacian(grey_frame, cv2.CV_64F).var() ##apply laplacian to greyscale image

######

    threshold = 0.01
    xy = find_intersections(HTlines, threshold)
    
    cv2.namedWindow('Original',cv2.WINDOW_NORMAL)
    cv2.imshow('Original',frame) 
    cv2.resizeWindow('Original', 900,500)

    # Display edges in a frame
    if HTlines is not None:
        for l in HTlines:
            cv2.line(line_copy,(l.x1,l.y1),(l.x2,l.y2),(0,0,255),2,cv2.LINE_AA)

    if xy is not None:
        for corner in xy:
            cv2.circle(line_copy, tuple(corner), 25, (0,255,0), 5)
        if (len(xy) == 1) : singleCornerCounter += 1
        else : singleCornerCounter = 0
    else : singleCornerCounter = 0

    cv2.putText(line_copy, "{}: {:.2f}".format("Variance of Laplacian: ", laplacianVar), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    if xy is not None : cv2.putText(line_copy, "{}: {:.2f}".format("Number of corners: ", len(xy)), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    else : cv2.putText(line_copy, "{}: {:.2f}".format("Number of corners = 0 "), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv2.putText(line_copy, "{}: {:.2f}".format("1 corner counter: " , singleCornerCounter), (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv2.putText(line_copy, "{}: {:.2f}".format("Number of HTlines: ", len(HTlines)), (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.namedWindow('Edges',cv2.WINDOW_NORMAL)    
    cv2.imshow('Edges',line_copy)
    cv2.resizeWindow('Edges', 900,500)

    if (singleCornerCounter == 1) : time.sleep(10)
#    if (singleCornerCounter == 3 and laplacianVar > 0.75) : time.sleep(10)
#    if (laplacianVar > 100) : time.sleep(10)

    key = cv2.waitKey(1) 
    if key == ('c'):
        continue


# Close the window
cap.release()
# De-allocate any associated memory usage
cv2.destroyAllWindows()

