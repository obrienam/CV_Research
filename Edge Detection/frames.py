import cv2

def FrameCaputre(path):
    vidObj = cv2.VideoCapture(path)
    count = 0
    success = 1
    while success:
        success, image = vidObj.read()
        cv2.imwrite("frame%d.jpg" % count, image)
        if __name__ == '__main__': 
  
    # Calling the function 
    FrameCapture("C:\\Users\\Admin\\PycharmProjects\\project_1\\openCV.mp4") 