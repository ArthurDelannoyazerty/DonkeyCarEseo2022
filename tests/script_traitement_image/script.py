#import argparse
import cv2 as cv
import sys
from cv2 import threshold
from cv2 import blur
import numpy as np




"""
max_value = 255
max_type = 4
max_binary_value = 255
trackbar_type = 'Type: \n 0: Binary \n 1: Binary Inverted \n 2: Truncate \n 3: To Zero \n 4: To Zero Inverted'
trackbar_value = 'Value'
window_name = 'Threshold Demo'

def Threshold_Demo(val):
    #0: Binary
    #1: Binary Inverted
    #2: Threshold Truncated
    #3: Threshold to Zero
    #4: Threshold to Zero Inverted
    threshold_type = cv.getTrackbarPos(trackbar_type, window_name)
    threshold_value = cv.getTrackbarPos(trackbar_value, window_name)
    _, dst = cv.threshold(gray, threshold_value, max_binary_value, threshold_type )
    cv.imshow(window_name, dst)

parser = argparse.ArgumentParser(description='Code for Basic Thresholding Operations tutorial.')
parser.add_argument('--input', help='Path to input image.', default='original_2k22.jpg')
args = parser.parse_args()
"""

##load imagesv
origin = cv.imread(cv.samples.findFile("1073_cam_image_array_.jpg"))
if origin is None:
    sys.exit("Could not read the image.")
"""
mask = cv.imread(cv.samples.findFile("mask.png"))
if mask is None:
    sys.exit("Could not read the image.")
"""
cv.imshow("0 - original", origin)



y=43
x=25
h=76
w=180
crop_img = origin[y:y+h, x:x+w]
cv.imshow("0.1 - masque numpy", crop_img)

##ajout masque
"""
e1 = cv.getTickCount()

wMask = cv.bitwise_and(origin,mask)

e2 = cv.getTickCount()
t = (e2 - e1)/cv.getTickFrequency()
print( "ajout mask  : ",t)

#cv.imshow("1 - mask", wMask)
"""
##niveau de gris
e1 = cv.getTickCount()

gray = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)

e2 = cv.getTickCount()

cv.imshow("2 - gray", gray)

t = (e2 - e1)/cv.getTickFrequency()
print( "gray  : " ,t)


"""
input_img = gray

e1 = cv.getTickCount()

contrast = 255
brightness = 100
if brightness != 0:
    if brightness > 0:
        shadow = brightness
        highlight = 255
    else:
        shadow = 0
        highlight = 255 + brightness
    alpha_b = (highlight - shadow)/255
    gamma_b = shadow
    buf = cv.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
else:
    buf = input_img.copy()
if contrast != 0:
    f = float(131 * (contrast + 127)) / (127 * (131 - contrast))
    alpha_c = f
    gamma_c = 127*(1-f)
    buf = cv.addWeighted(buf, alpha_c, buf, 0, gamma_c)
        
bright = buf

e2 = cv.getTickCount()
t = (e2 - e1)/cv.getTickFrequency()
print( "bright  : " ,t)

cv.imshow("2.? - brigth", bright)
"""





#blur

e1 = cv.getTickCount()
i=5
blured = cv.GaussianBlur(gray, (i, i), 0)

t = (e2 - e1)/cv.getTickFrequency()
print( "blur  : " ,t)

cv.imshow("2.0.5 - bilateral filter", blured)



#threshold
"""
e1 = cv.getTickCount()

_,thresholdImage = cv.threshold(gray, 200, 255, type=cv.THRESH_TOZERO)

e2 = cv.getTickCount()

cv.imshow("2.1 - treshold tozero", thresholdImage)

t = (e2 - e1)/cv.getTickFrequency()
print( "tozero  : " ,t)
"""



# edge
e1 = cv.getTickCount()
edges = cv.Canny(blured,100,200)

e2 = cv.getTickCount()
t = (e2 - e1)/cv.getTickFrequency()
print( "edges  : " ,t)

cv.imshow("2.0.6 - canny detection", edges)

##noir & blanc --> fait par threshold
"""
e1 = cv.getTickCount()
(thresh, blackAndWhiteImage) = cv.threshold(thresholdImage, 127, 255, cv.THRESH_BINARY)

e2 = cv.getTickCount()
t = (e2 - e1)/cv.getTickFrequency()
print( "black & white  : ",t)

cv.imshow("2.1 - noir/blanc", blackAndWhiteImage)
"""

# adaptive threshold
e1 = cv.getTickCount()
thresholdImage = cv.adaptiveThreshold(edges, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

e2 = cv.getTickCount()
t = (e2 - e1)/cv.getTickFrequency()
print( "adaptive  : " ,t)

cv.imshow("2.0..x : adaptive threshold", thresholdImage)




##erosion/dilation
"""
e1 = cv.getTickCount()

kernel_size = 2     #3,5,7 aua choix
kernel = np.ones((kernel_size,kernel_size),np.uint8)
#kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(kernel_size,kernel_size))
#kernel = cv.getStructuringElement(cv.MORPH_CROSS,(kernel_size,kernel_size))

erosion = cv.erode(edges,kernel,iterations = 1)
dilatation_dst = cv.dilate(erosion, kernel, iterations=1)
#erosion = cv.erode(blackAndWhiteImage,cv.MORPH_OPEN,kernel)

e2 = cv.getTickCount()
t = (e2 - e1)/cv.getTickFrequency()
print( "erosion  : ", t )

cv.imshow("2.2 - erosion", erosion)
"""

## couleur
e1 = cv.getTickCount()
couleur = cv.cvtColor(edges, cv.COLOR_GRAY2RGB)
cv.imshow("3", couleur)

e2 = cv.getTickCount()
t = (e2 - e1)/cv.getTickFrequency()
print( "gray2rgb  : ", t )




cv.waitKey()

"""
cv.namedWindow(window_name)
cv.createTrackbar(trackbar_type, window_name , 3, max_type, Threshold_Demo)
# Create Trackbar to choose Threshold value
cv.createTrackbar(trackbar_value, window_name , 0, max_value, Threshold_Demo)
# Call the function to initialize
Threshold_Demo(0)
# Wait until user finishes program
cv.waitKey()
"""

"""
##threshold avec moyenne
adapt = cv.adaptiveThreshold(blackAndWhiteImage, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2)
cv.imshow("3 - adaptive_mean_binary_inv", adapt)
k = cv.waitKey(0)
"""