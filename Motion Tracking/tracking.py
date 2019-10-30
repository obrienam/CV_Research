import cv2
from random import randint
import numpy as np
if __name__ == '__main__':
    im=cv2.imread("../Assets/image282.jpg")
    r=cv2.selectROI(im)