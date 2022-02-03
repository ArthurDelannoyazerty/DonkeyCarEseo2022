import cv2 as cv
import sys
import numpy as np



##load imagesv
origin = cv.imread(cv.samples.findFile("original_2k22.jpg"))
if origin is None:
    sys.exit("Could not read the image.")

mask = cv.imread(cv.samples.findFile("mask.png"))
if mask is None:
    sys.exit("Could not read the image.")

cv.imshow("0 - original", origin)



y=43
x=25
h=76
w=180
crop_img = origin[y:y+h, x:x+w]
cv.imshow("0.1 - masque numpy", crop_img)

##ajout masque
e1 = cv.getTickCount()

#wMask = cv.bitwise_and(origin,mask)


e2 = cv.getTickCount()
t = (e2 - e1)/cv.getTickFrequency()
print( "ajout mask  : ",t)

#cv.imshow("1 - mask", wMask)

##niveau de gris
e1 = cv.getTickCount()

gray = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)
cv.imshow("2 - gray", gray)

e2 = cv.getTickCount()
t = (e2 - e1)/cv.getTickFrequency()
print( "gray  : " ,t)


##noir & blanc
(thresh, blackAndWhiteImage) = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

e2 = cv.getTickCount()
t = (e2 - e1)/cv.getTickFrequency()
print( "black & white  : ",t)

cv.imshow("2.1 - noir/blanc", blackAndWhiteImage)

##erosion
e1 = cv.getTickCount()

kernel_size = 3     #3,5,7 aua choix
#kernel = np.ones((kernel_size,kernel_size),np.uint8)
#kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(kernel_size,kernel_size))
kernel = cv.getStructuringElement(cv.MORPH_CROSS,(kernel_size,kernel_size))

erosion = cv.erode(blackAndWhiteImage,kernel,iterations = 1)
#erosion = cv.erode(blackAndWhiteImage,cv.MORPH_OPEN,kernel)

e2 = cv.getTickCount()
t = (e2 - e1)/cv.getTickFrequency()
print( "erosion  : ", t )

cv.imshow("2.2 - erosion", erosion)
k = cv.waitKey(0)


"""
##threshold avec moyenne
adapt = cv.adaptiveThreshold(blackAndWhiteImage, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2)
cv.imshow("3 - adaptive_mean_binary_inv", adapt)
k = cv.waitKey(0)
"""