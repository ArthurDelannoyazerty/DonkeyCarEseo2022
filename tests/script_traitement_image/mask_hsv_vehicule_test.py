import numpy as np
import cv2

origin = cv2.imread(cv2.samples.findFile("circuit_normal1.jpg"))

lower_black = np.array([0,0,0], dtype = "uint16")
upper_black = np.array([70,70,70], dtype = "uint16")
black_mask = cv2.inRange(origin, lower_black, upper_black)
cv2.imshow('mask0',black_mask)

cv2.waitKey()