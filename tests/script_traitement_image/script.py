import cv2 as cv
import sys




##load images
origin = cv.imread(cv.samples.findFile("original.jpg"))
if origin is None:
    sys.exit("Could not read the image.")

mask = cv.imread(cv.samples.findFile("mask.png"))
if mask is None:
    sys.exit("Could not read the image.")

cv.imshow("0 - original", origin)

##ajout masque
wMask = cv.bitwise_and(origin,mask)
cv.imshow("1 - mask", wMask)

##niveau de gris
gray = cv.cvtColor(wMask, cv.COLOR_BGR2GRAY)
cv.imshow("2 - Color conversion brg to gray + mask", gray)

##threshold avec moyenne
adapt = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2)
cv.imshow("3 - Color conversion brg to gray + adaptive tresh mean + mask", adapt)
k = cv.waitKey(0)
