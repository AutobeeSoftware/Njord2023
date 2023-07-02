import cv2
import numpy as np
from utils2 import gstreamer_pipeline


def camCombine(frameL,frameR,overlap):
   
    if frameL.shape[0] == frameR.shape[0] and frameL.shape[1] == frameR.shape[1]:
        h = frameL.shape[0]
        w = frameR.shape[1]
        frameL = frameL[:h, : w - overlap] 
        frameR = frameR[:h, overlap :]

        combined_frame = np.hstack((frameL, frameR))


        return combined_frame

    else:
        return None





frame1 = cv2.VideoCapture(gstreamer_pipeline(0))
frame2 = cv2.VideoCapture(gstreamer_pipeline(1))

ret1, frameL = frame1.read()
ret2, frameR = frame2.read()

width = frameL.shape[1]
heigth = frameL.shape[0]
print((width,heigth))





def empty(img):
    pass

cv2.namedWindow("TrackBar")  
cv2.resizeWindow("TrackBar", heigth+30, width*2, )
cv2.createTrackbar("overlap", "TrackBar", 0, width*2, empty)




while True:  

    ret1, frameL = frame1.read()
    ret2, frameR = frame2.read()

    overlap = cv2.getTrackbarPos("overlap", "TrackBar")


    combined = camCombine(frameL, frameR,overlap)

    cv2.putText(combined, "left cam", (int(0), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(combined, "right cam" , (int(width-10), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    

    cv2.imshow("TrackBar", combined)  
    cv2.getTrackbarPos("TrackBar", "Frame")
    k = cv2.waitKey(1)  
    
    if k == ord('q'):  
        break
    
    if k == ord('s'):  
        print("overlap: " + str(overlap))


ret1.release()
ret2.release()

cv2.destroyAllWindows()
