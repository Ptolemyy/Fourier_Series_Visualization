import cv2
import numpy as np

img = cv2.imread("happy.png")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours_img = np.zeros(img.shape[:], dtype=np.uint8)
contours_img[:] = 255


cv2.drawContours(contours_img,contours,-1,(0,0,0),1)
cv2.imwrite("3.jpg",contours_img)