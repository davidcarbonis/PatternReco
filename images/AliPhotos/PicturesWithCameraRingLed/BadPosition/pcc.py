import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(2)
y=" Done!"
i=0
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

    if key == ord('p'): # exit on ESC
        cv2.imwrite('opcv'+ str(i) +'.png',frame)
		
	i=i+1
	print(str(i)+y)
		
cv2.destroyWindow("preview")
vc.release()