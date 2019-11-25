import cv2
import numpy as np
import sys

vs=cv2.VideoCapture("C:/Users/obrienam/Documents/GitHub/CV_Research/Assets/bees2.mp4")

frame_width = int(vs.get(3))
frame_height = int(vs.get(4))
out = cv2.VideoWriter('contrast.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
while True:
    hasFrames,frame=vs.read()
    if (hasFrames==False):
        break
    for y in range(frame.shape[0]):
        for x in range(frame.shape[1]):
            for c in range(frame.shape[2]):
                frame[y,x,c]=np.clip(2*frame[y,x,c] + 0, 0, 255)
    key=cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    out.write(frame)
vs.release()
cv2.destroyAllWindows()


