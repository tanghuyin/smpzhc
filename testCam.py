import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
FRONT_CAM = 1
BACK_CAM = 0


skeletonArray = [  0,0,1,1,0,0,1,1,1,1,0,1,1,1,0,1,\

        1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,1,\

         0,0,1,1,0,0,1,1,1,1,0,1,1,1,0,1,\

        1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,1,\

        1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,\

        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\

        1,1,0,0,1,1,0,0,1,1,0,1,1,1,0,1,\

        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\

        0,0,1,1,0,0,1,1,1,1,0,1,1,1,0,1,\

        1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,1,\

        0,0,1,1,0,0,1,1,1,1,0,1,1,1,0,1,\

        1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,\

         1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,\

        1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,\

        1,1,0,0,1,1,0,0,1,1,0,1,1,1,0,0,\

        1,1,0,0,1,1,1,0,1,1,0,0,1,0,0,0]

def startFrontCam():
    frontCam = cv2.VideoCapture(FRONT_CAM)
    return frontCam


def startBackCam():
    backCam = cv2.VideoCapture(BACK_CAM)
    return backCam


def startCam(Cam_No):
    if Cam_No == FRONT_CAM:
        print("start front camera")
        c = startFrontCam()
        return c
    elif Cam_No == BACK_CAM:
        c = startBackCam()
        return c


def showCamVideo(camera, mode): #mode means xunxian==0 or daoche==1
    while(1):
        # count += 1
        _, CamVideo = camera.read()
        result = preProcessing(CamVideo)
        # result = skeleton(result, skeletonArray)
        curve = []
        path = []
        for line in range(result.shape[0]):
            change, pos = lineByLine(result, line)
            path.append(pos)
        path = pathProcessing(path)
        result = drawPath(result, path)
        cv2.imshow("capture", result)
        # cv2.imwrite("testcross.jpg", result)
        # break
        # saveName = "video" + str(count) + ".jpg"
        # cv2.imwrite(saveName, result)
        # time.sleep(0.2)
        if cv2.waitKey(1) == 27:     # "ESC" ASCII is 27
            break
        
# Let's look look how the camera behave in the real situation, then think an appropriate algorithom, apply it on "result"

def drawPath(img, path):
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for i in range(len(path)):
        img[len(path)-i-1, path[i]] = [0,255,0]
    return img

def preProcessing(img):
    img = img[400:480, 200:400]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.pyrDown(gray, (50, 125))
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # Since the car is on a white board with black line, OTSU binary may work well.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    
    # print(_) # threshold
    return closing


def pathProcessing(path):
    centers = []
    if len(path[-1]) == 2:
        last_center = int((path[-1][0] + path[-1][1]) / 2)
        centers.append(last_center)
    else:
        last_center = 0
    for i in range(len(path)-2, 0, -1):
        center = []
        true_center = 0
        smallest_delta = 9999
        pair_num = int(len(path[i]) / 2)
        for pair in range(pair_num):
            center.append(int((path[i][pair*2] + path[i][pair*2+1]) / 2))
        for c in center:
            if abs(c - last_center) < smallest_delta:
                true_center = c
                smallest_delta = abs(c - last_center)
        last_center = true_center
        centers.append(true_center)
    return centers

def skeleton(image,array):
    h,w = image.shape
    iThin = image
 
    for i in range(h):
        for j in range(w):
            if image[i,j] == 0:
                a = [1]*9
                for k in range(3):
                    for l in range(3):
                        if -1<(i-1+k)<h and -1<(j-1+l)<w and iThin[i-1+k,j-1+l]==0:
                            a[k*3+l] = 0
                sum = a[0]*1+a[1]*2+a[2]*4+a[3]*8+a[5]*16+a[6]*32+a[7]*64+a[8]*128
                iThin[i,j] = array[sum]*255
    return iThin  
    
def lineByLine(img, line):
    change = 0
    linePixel = img[line, :]
    init = linePixel[0]
    pos = []
    for i in range(linePixel.shape[0] - 1):
        if linePixel[i] != init:
            change += 1
            init = linePixel[i]
            pos.append(i)
    return change, pos

def releaseCam(camera):
    camera.release()


def main():
    frontCamera = startCam(FRONT_CAM)
    showCamVideo(frontCamera, 0)
    releaseCam(frontCamera)
    cv2.destroyAllWindows()

main()
