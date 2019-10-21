import cv2 as cv
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import time
import imutils
brownLower = (101,84,33)
brownUpper = (101,56,33)
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

cv.destroyAllWindows()