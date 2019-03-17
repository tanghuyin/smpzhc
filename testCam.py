import cv2
import numpy as np
#add camera
cap=cv2.VideoCapture(0)
#open camera
while(1):    # get a frame   
    ret, frame = cap.read()    # show a frame   
    cv2.imshow("capture", frame)   
    if cv2.waitKey(1) & 0xFF == ord('q'):        
        break
cap.release()
cv2.destroyAllWindows()



'''import cv2
import numpy as np

frontCam = cv2.VideoCapture(0)
frontCam.open(0)
ret, frame = frontCam.read()
cv2.namedWindow("test")
while True:
    cv2.imshow("test", frame)
    ret, frame = frontCam.read()


cv.destroyAllWindows()
frontCam.release()
'''
