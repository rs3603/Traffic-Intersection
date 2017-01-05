import numpy as np
import cv2


cap = cv2.VideoCapture('/home/raghavendra/Desktop/NVIDIA_Research/GOPR0077.avi')
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorMOG2()
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video = cv2.VideoWriter("rec_out.avi", fourcc, 20, (1920, 1080))
while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    se = np.ones((7,7), dtype='uint8')
    image_close = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, se)
    img = frame
    rows,cols,ch = img.shape
    print rows,cols
    pts1 = np.float32([[546,285],[500,518],[748,279]])
    pts2 = np.float32([[546,365],[736,618],[748,279]])
    M = cv2.getAffineTransform(pts2,pts1)
    #M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
    dst = cv2.warpAffine(img,M,(cols,rows))

    pts1 = np.float32([[546,285],[500,518],[748,279],[700,570]])
    pts2 = np.float32([[546,285],[500,518],[748,279],[780,550]])
    M = cv2.getPerspectiveTransform(pts2,pts1)
    dst2 = cv2.warpPerspective(dst,M,(cols,rows))
    #video = cv2.VideoWriter('video.avi',-1,1,(cols,rows))
    video.write(dst2)
    cv2.imshow('frame',dst2)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
video.release()
