import cv2
import matplotlib.pyplot as plt
import math
import numpy as np
def upContrast(image,alpha,beta):
    n_image = np.zeros(image.shape, image.dtype)

    alpha=1.0
    beta=0

    alpha=float(1)
    beta=float(0)

    n_image=np.multiply(image,2)

   
    return n_image
def countStill(img1, img2):
    m=0
    bk = cv2.imread('../Assets/bee-backgroundcontrast.png')
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
bev="Steady"
s=0
frame_width = int(vs.get(3))
frame_height = int(vs.get(4))
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
while True:
    hasFrames,frame=vs.read()
    if (hasFrames==False):
        break
    
    if firstFrame is not None:
        #frame=upContrast(frame,2,1)
        s=countStill(firstFrame,frame)
        
        if(prev_s is None):
            bev="Steady"
        elif(prev_s<s):  
            bev="Increasing"
        elif(prev_s==s):
            bev="Steady" 
        elif(prev_s>s):
            bev="Decreasing"   
        prev_s=s
        firstFrame=frame
    else:    
        firstFrame=frame
    key=cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    
    
    cv2.putText(frame, "Stationary Bees: {}".format(bev), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("vid",frame)
    out.write(frame)
vs.release()
cv2.destroyAllWindows()

    