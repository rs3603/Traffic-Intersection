import numpy as np
import cv2

#cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture('rec_out.wmv')
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorMOG2(history=50000, varThreshold = 1)
ret, framebg = cap.read()
framebg = (cv2.cvtColor(framebg, cv2.COLOR_BGR2GRAY))
'''
ret, framebg1 = cap.read()
framebg1 = cv2.equalizeHist(cv2.cvtColor(framebg1, cv2.COLOR_BGR2GRAY))
ret, framebg2 = cap.read()
framebg = (cv2.cvtColor(framebg2, cv2.COLOR_BGR2GRAY))
ret, framebg2 = cap.read()
framebg = (cv2.cvtColor(framebg2, cv2.COLOR_BGR2GRAY))
ret, framebg2 = cap.read()
framebg = (cv2.cvtColor(framebg2, cv2.COLOR_BGR2GRAY))
ret, framebg2 = cap.read()
framebg = (cv2.cvtColor(framebg2, cv2.COLOR_BGR2GRAY))
ret, framebg2 = cap.read()
framebg = (cv2.cvtColor(framebg2, cv2.COLOR_BGR2GRAY))
ret, framebg2 = cap.read()
framebg = (cv2.cvtColor(framebg2, cv2.COLOR_BGR2GRAY))
ret, framebg2 = cap.read()
framebg = (cv2.cvtColor(framebg2, cv2.COLOR_BGR2GRAY))
ret, framebg2 = cap.read()
framebg = (cv2.cvtColor(framebg2, cv2.COLOR_BGR2GRAY))
ret, framebg2 = cap.read()
framebg = (cv2.cvtColor(framebg2, cv2.COLOR_BGR2GRAY))
'''
while(1):
    ret, frame = cap.read()
    cap.set(cv2.CAP_PROP_FPS,200)

    img_gray = (cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    #print img_yuv
    # equalize the histogram of the Y channel
    #img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])

    # convert the YUV image back to RGB format
    #frame = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    fgmask = abs(img_gray-framebg)%255
    #indices = fgmask > 0
    #fgmask[indices] = 255
    #print fgmask.astype(dtype='uint8')
    se = np.ones((7,7), dtype='uint8')
    kernel = np.ones((7,7),np.uint8)
    fgmask = cv2.morphologyEx(fgmask.astype(dtype = 'uint8'), cv2.MORPH_OPEN, se)
    im2, contours, hierarchy = cv2.findContours(fgmask.astype(dtype = 'uint8'),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    indices = fgmask>200
    fgmask[indices] = 0
    thresh = cv2.threshold(fgmask, 5, 255, cv2.THRESH_BINARY)[1]
    threshnew = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, se)
    im2, contours, hierarchy = cv2.findContours(threshnew,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        rect = cv2.boundingRect(c)
        if cv2.contourArea(c)>300: 
            #print cv2.contourArea(c)
            x,y,w,h = rect
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            #cv2.putText(frame,'Car',(x+w+10,y+h),0,0.3,(0,255,0))
        if cv2.contourArea(c)>5 and cv2.contourArea(c)<70 and rect[2]>5 and rect[3]>5: 
            #print cv2.contourArea(c)
            x,y,w,h = rect
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            #cv2.putText(frame,'Pedestrian',(x+w+10,y+h),0,0.3,(0,0,255))
    cv2.imshow("Show",frame)

    #print len(contours)    
    #cv2.drawContours(fgmask, contours, 3, (0,255,0), 3)
    se = np.ones((7,7), dtype='uint8') 
    #cv2.imshow('frame',fgmask)
    #cv2.imshow('frame1',im2)
    k = cv2.waitKey(20) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
