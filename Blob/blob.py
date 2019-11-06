import cv2
import numpy as np;

image1 = cv2.imread("../Assets/image287.jpg")
og = image1.copy()
diff=abs(image1-og)

median = np.median(image1[image1>0])
mask=image1.copy()
mask[mask > median+0.07]=0
mask[mask < median+0.07]=0
mask[mask > 0]=1

_,contours,_=cv2.findContours(mask,2,1)
contours=sorted(contours,key=cv2.countourArea)
out_mask=np.zeros_like(image1)

cv2.drawContours(out_mask, [contours[-1]],-1,255,cv2.FILLED, 1)

out=image1.copy()
out[out_mask==0]=0