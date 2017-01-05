import numpy as np
import cv2

#cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture('rec_out.wmv')
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorMOG2()
ret, frame = cap.read()
i = 0
while(1):
    i = i + 1
    ret, frame = cap.read()
    frame1 = frame
    cap.set(cv2.CAP_PROP_FPS,200)

    img_yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)

    # equalize the histogram of the Y channel
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])

    # convert the YUV image back to RGB format
    frame = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    fgmask = fgbg.apply(frame)
    print fgmask.shape
    se = np.ones((3,3), dtype='uint8')
    kernel = np.ones((7,7),np.uint8)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, se)
    im2, contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    car_positions = []
    ped_positions = []
    for c in contours:
        rect = cv2.boundingRect(c)
        if cv2.contourArea(c)>500: 
            #print cv2.contourArea(c)
            x,y,w,h = rect
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            #cv2.putText(frame,'Car',(x+w+10,y+h),0,0.3,(0,255,0))
            car_positions.append([x,y,w,h])
        else:
            car_positions.append([None,None,None,None])
        if cv2.contourArea(c)>50 and cv2.contourArea(c)<70 and rect[2]>5 and rect[3]>5: 
            #print cv2.contourArea(c)
            x,y,w,h = rect
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            #print x,y
            #cv2.putText(frame,'Pedestrian',(x+w+10,y+h),0,0.3,(0,0,255))
            ped_positions.append([x,y,w,h])
        else:
            ped_positions.append([None,None,None,None])
    cv2.imshow("Show",frame)
    #print len(contours)    
    #cv2.drawContours(fgmask, contours, 3, (0,255,0), 3)
    se = np.ones((7,7), dtype='uint8') 
    #cv2.imshow('frame',fgmask)
    #cv2.imshow('frame1',im2)
    k = cv2.waitKey(20) & 0xff
    if k == 27:
        print car_positions
        print ped_positions
        break

cap.release()
cv2.destroyAllWindows()
