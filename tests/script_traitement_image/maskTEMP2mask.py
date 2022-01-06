import cv2 as cv
import sys





img = cv.imread(cv.samples.findFile("maskTEMP.jpg"))
if img is None:
    sys.exit("Could not read the image.")

cv.imshow("maskTEMP", img)
k = cv.waitKey(0)

img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow("mask", img)
k = cv.waitKey(0)
ret, img = cv.threshold(img, 10, 255, cv.THRESH_BINARY)
#cv.imshow("mask", img)
k = cv.waitKey(0)
#img = cv.bitwise_not(img)
#cv.imshow("mask", img)
#k = cv.waitKey(0)
#img = cv.bitwise_and(img, img, mask = img)
#cv.imshow("mask", img)
#cv.waitKey(0)

cv.imwrite("mask.png", img)