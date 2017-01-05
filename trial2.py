import numpy as np
import cv2


cap = cv2.VideoCapture('/home/raghavendra/Desktop/NVIDIA_Research/output.avi')
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorMOG2()
while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    se = np.ones((7,7), dtype='uint8')
    #fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, se)
    im2, contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        rect = cv2.boundingRect(c)
        car_contours = []
        ped_contours = []
        if cv2.contourArea(c)>400: 
            print cv2.contourArea(c)
            x,y,w,h = rect
            x_c,y_c,w_c,h_c = rect
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            #cv2.putText(frame,'Car',(x+w+10,y+h),0,0.3,(0,255,0))
        if cv2.contourArea(c)>10 and cv2.contourArea(c)<70 and rect[2]>5 and rect[3]>5: 
            print cv2.contourArea(c)
            x,y,w,h = rect
            if (x>x_c and x+w<x_c+w_c and y<y_c and y+h<y_c+h_c):
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),2)
            else:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            #cv2.putText(frame,'Pedestrian',(x+w+10,y+h),0,0.3,(0,0,255))
    cv2.imshow("Show",frame)

    #print len(contours)    
    #cv2.drawContours(fgmask, contours, 3, (0,255,0), 3)
    se = np.ones((7,7), dtype='uint8') 
    cv2.imshow('frame',fgmask)
    #cv2.imshow('frame1',im2)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
