from __future__ import print_function
from __future__ import division
import cv2 as cv
import argparse


title_window = 'Cropping images'
val = [0,0,10,10] #y,height,x,width

def move():
    crop_img = src1[val[0]:val[0]+val[1], val[2]:val[2]+val[3]]
    cv.imshow("croped", crop_img)

def on_trackbar1(offset_x):
    val[2] = offset_x
    move()

def on_trackbar2(offset_y):
    val[0] = offset_y
    move()

def on_trackbar3(height):
    val[1] = height
    move()

def on_trackbar4(width):
    val[3] = width
    move()


src1 = cv.imread(cv.samples.findFile("original.jpg"))
if src1 is None:
    print('Could not open or find the image: ')
    exit(0)


cv.namedWindow(title_window)

max_offset_x = src1.shape[1]-1
max_offset_y = src1.shape[0]-1
max_width    = src1.shape[1]-1
max_height   = src1.shape[0]-1

trackbar_name1 = 'Off X  x %d' % max_offset_x
trackbar_name2 = 'Off Y  x %d' % max_offset_y
trackbar_name3 = 'Width  x %d' % max_width
trackbar_name4 = 'Height x %d' % max_height

cv.createTrackbar(trackbar_name1, title_window , 0              , max_offset_x, on_trackbar1)
cv.createTrackbar(trackbar_name2, title_window , 0              , max_offset_y, on_trackbar2)
cv.createTrackbar(trackbar_name3, title_window , src1.shape[1]  , max_width   , on_trackbar4)
cv.createTrackbar(trackbar_name4, title_window , src1.shape[0]  , max_height  , on_trackbar3)
# Show some stuff
on_trackbar1(0)
on_trackbar2(0)
on_trackbar3(src1.shape[0]-1)
on_trackbar4(src1.shape[1]-1)
# Wait until user press some key
cv.waitKey()