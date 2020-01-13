import cv2
import numpy as np;
cap = cv2.VideoCapture("C:/Users/obrienam/Documents/GitHub/CV_Research/Assets/fanvid_1.mp4")
while True:
    ret,frame = cap.read()
    if ret==True:
        params=cv2.SimpleBlobDetector_Params()
        '''params.minThreshold=10
        params.maxThreshold=200
        params.filterByArea=True
        params.minArea=1500
        params.filterByCircularity=True
        params.minCircularity=0.1'''
        params.filterByConvexity=True
        params.minConvexity=0.4
        params.filterByInertia=True
        params.minInertiaRatio=0.8
        detector=cv2.SimpleBlobDetector_create(params)
        keypoints=detector.detect(frame)
        img=frame.copy()
        for x in range(1,len(keypoints)):
            img=cv2.circle(img, (np.int(keypoints[x].pt[0]),np.int(keypoints[x].pt[1])), radius=np.int(keypoints[x].size), color=(255), thickness=-1)
        cv2.imshow("blob",img)
        key=cv2.waitKey(30)

        
cap.release()
cv2.destroyAllWindows()