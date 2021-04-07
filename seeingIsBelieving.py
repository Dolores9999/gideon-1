
import cv2

import numpy as np

cap=  cv2.VideoCapture()
cap.open('http://dmrd:Erasure1969@192.168.1.10:8081')

while True:
  ret, frame=cap.read()



  cv2.imshow('gray',frame)
  cv2.waitKey(0)


cap.release()

cv2.destroyAllWindows
