from __future__ import print_function
from __future__ import division
import cv2 as cv
import argparse

alpha_slider_max = 254
beta_slider_max = 254
title_window = 'treshhold'

def on_trackbar(val):
    #alpha = val / alpha_slider_max
    ret,dst = cv.threshold(img,val,255,cv.THRESH_BINARY)
    cv.imshow(title_window, dst)


def trackbar_adaptive(val):
    #alpha = val / alpha_slider_max
    ret,dst = cv.Canny(img,100,200)
    cv.imshow(title_window, dst)

img = cv.imread(cv.samples.findFile("original.jpg"))
if img is None:
    sys.exit("Could not read the image.")


cv.namedWindow(title_window)
trackbar_name = 'tresh_binary x %d' % alpha_slider_max
cv.createTrackbar(trackbar_name, title_window , 0, alpha_slider_max, on_trackbar)


trackbar_name2 = 'beta x %d' % beta_slider_max
cv.createTrackbar(trackbar_name2, title_window , 0, beta_slider_max, trackbar_adaptive)


# Show some stuff
on_trackbar(0)
# Wait until user press some key
cv.waitKey()