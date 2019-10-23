import cv2 as cv
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import time
import imutils
brownLower = (101,84,33)
brownUpper = (101,56,33)
pts=deque(maxlen=256)
counter=0
cap = cv.VideoCapture("../Assets/bees1.mp4")
while True:
    frame=cap.read()
    frame=frame[1]
    if frame is None:
        break

    frame=imutils.resize(frame,width=600)
    blurred=cv.GaussianBlur(frame,(11,11),0)
    hsv=cv.cvtColor(blurred, cv.COLOR_BGR2HSV)


    mask=cv.inRange(hsv, brownLower, brownUpper)
    mask=cv.erode(mask,None,iterations=2)
    mask=cv.dilate(mask, None, iterations=2)


    cnts=cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts=imutils.grab_contours(cnts)
    center=None

    if len(cnts) > 0:
        c=max(cnts, key=cv.contourArea)
        ((x,y),radius) = cv.minEnclosingCircle(c)
        M=cv.moments(c)
        center=(int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        if radius > 10:
            cv.circle(frame, (int(x),int(y)),int(radius),(0,255,255),2)
            cv.circle(frame,center,5,(0,0,255),-1)
            pts.appendleft(center)
    for i in np.arange(1, len(pts)):
    # if either of the tracked points are None, ignore
    # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # check to see if enough points have been accumulated in
        # the buffer
        if counter >= 10 and i == 1 and pts[-10] is not None:
            # compute the difference between the x and y
            # coordinates and re-initialize the direction
            # text variables
            dX = pts[-10][0] - pts[i][0]
            dY = pts[-10][1] - pts[i][1]
            (dirX, dirY) = ("", "")

            # ensure there is significant movement in the
            # x-direction
            if np.abs(dX) > 20:
                dirX = "East" if np.sign(dX) == 1 else "West"

            # ensure there is significant movement in the
            # y-direction
            if np.abs(dY) > 20:
                dirY = "North" if np.sign(dY) == 1 else "South"

            # handle when both directions are non-empty
            if dirX != "" and dirY != "":
                direction = "{}-{}".format(dirY, dirX)

            # otherwise, only one direction is non-empty
            else:
                direction = dirX if dirX != "" else dirY
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(256 / float(i + 1)) * 2.5)
            cv.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
        # show the movement deltas and the direction of movement on
        # the frame
        cv.putText(frame, direction, (10, 30), cv.FONT_HERSHEY_SIMPLEX,
            0.65, (0, 0, 255), 3)
        cv.putText(frame, "dx: {}, dy: {}".format(dX, dY),
            (10, frame.shape[0] - 10), cv.FONT_HERSHEY_SIMPLEX,
            0.35, (0, 0, 255), 1)
    
        # show the frame to our screen and increment the frame counter
        cv.imshow("Frame", frame)
        key = cv.waitKey(1) & 0xFF
        counter += 1
    
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
 
# otherwise, release the camera
else:
	cap.release()
 
# close all windows
cv.destroyAllWindows()