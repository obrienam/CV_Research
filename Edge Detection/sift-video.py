import cv2
import matplotlib.pyplot as plt
import math

def upContrast(img1,img2,)
def countStill(img1, img2):
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
                print("match")
                break
        
    pt=keypoints_1[0].pt

vs=cv2.VideoCapture("/Users/aidanobrien/Documents/GitHub/CV_Research/Assets/bees2.mp4")
firstFrame=None
while True:
    hasFrames,frame=vs.read()
    if (hasFrames==False):
        break
    cv2.imshow("vid",frame)
    if firstFrame is not None:
        
    key=cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    firstFrame=frame

vs.release()
cv2.destroyAllWindows()

    