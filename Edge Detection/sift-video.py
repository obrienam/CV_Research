import cv2
import matplotlib.pyplot as plt
import math
import numpy as np
def upContrast(img1,img2,alpha,beta):
    n_image1 = np.zeros(img1.shape, img1.dtype)
    n_image2 = np.zeros(img2.shape, img2.dtype)
    for y in range(img1.shape[0]):
        for x in range(img1.shape[1]):
            for c in range(img1.shape[2]):
                n_image1[y,x,c]=np.clip(alpha*img1[y,x,c] + beta, 0, 255)
    for y in range(img2.shape[0]):
        for x in range(img2.shape[1]):
            for c in range(img2.shape[2]):
                n_image2[y,x,c]=np.clip(alpha*img2[y,x,c] + beta, 0, 255)
    return n_image1,n_image2
def countStill(img1, img2):
    m=0
    bk = cv2.imread('../Assets/bee-background.png')
    subImage1=(bk.astype('int32')-img1.astype('int32')).clip(0).astype('uint8')
    grey1=cv2.cvtColor(subImage1,cv2.COLOR_BGR2GRAY)
    retval1,thresh1=cv2.threshold(grey1,35,255,cv2.THRESH_BINARY_INV)
    img1=grey1

    subImage2=(bk.astype('int32')-img2.astype('int32')).clip(0).astype('uint8')
    grey2=cv2.cvtColor(subImage2,cv2.COLOR_BGR2GRAY)
    retval2,thresh2=cv2.threshold(grey2,35,255,cv2.THRESH_BINARY_INV)
    img2=grey2

    #sift
    sift = cv2.xfeatures2d.SIFT_create()

    keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)
    kp1=keypoints_1
    kp2=keypoints_2
    d_1=descriptors_1
    d_2=descriptors_2
    #feature matching
    bf = cv2.BFMatcher()

    matches = bf.match(d_1,d_2)
    matches = sorted(matches, key = lambda x:x.distance)

    for i in range(len(kp1)):
        for j in range(len(kp2)):
            #print(kp2[j].pt[0])
            #print(kp2[j].pt[1])
            
            if(abs(kp1[i].pt[0]-kp2[j].pt[0])<2 and abs(kp1[i].pt[1]-kp2[j].pt[1])<4):
                m+=1
                break
        
    pt=keypoints_1[0].pt
    return m

vs=cv2.VideoCapture("C:/Users/obrienam/Documents/GitHub/CV_Research/Assets/bees2.mp4")
firstFrame=None
prev_s=None
while True:
    hasFrames,frame=vs.read()
    if (hasFrames==False):
        break
    cv2.imshow("vid",frame)
    if firstFrame is not None:
        s=countStill(firstFrame,frame)
        if(prev_s is None):
            prev_s=s
        if(prev_s<s):
            prev_s=s
            print(s)    
    
    key=cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    firstFrame=frame

vs.release()
cv2.destroyAllWindows()

    