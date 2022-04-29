#import argparse
import cv2 as cv
import sys
import numpy as np

##load imagesv
def loadImg(nom = "circuit_normal1.jpg"):
    origin = cv.imread(cv.samples.findFile(nom))
    if origin is None:
        sys.exit("Could not read the image.")
    cv.imshow("0 - original", origin)
    return origin

def crop(img,x=0,y=43,h=82,w=215):
    origin = img
    crop_img = origin[y:y+h, x:x+w]
    cv.imshow("Crop", crop_img)
    return crop_img

##ajout masque
"""
e1 = cv.getTickCount()

wMask = cv.bitwise_and(origin,mask)

e2 = cv.getTickCount()
t = (e2 - e1)/cv.getTickFrequency()
print( "ajout mask  : ",t)

#cv.imshow("1 - mask", wMask)
"""

def bgr2gray(crop_img):
    e1 = cv.getTickCount()
    gray = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)
    e2 = cv.getTickCount()
    cv.imshow("2 - gray", gray)
    t = (e2 - e1)/cv.getTickFrequency()

    return gray, t

def GaussianBlur(gray,i):
    e1 = cv.getTickCount()
    #i=5
    blured = cv.GaussianBlur(gray, (i, i), 0)
    e2 = cv.getTickCount()
    t = (e2 - e1)/cv.getTickFrequency()
    cv.imshow("gaussian blur", blured)

    return blured, t

def threshold(gray, type):
    if(type=="binaire"):
        type = cv.THRESH_BINARY
    elif(type=="binaire inv"):
        type=cv.THRESH_BINARY_INV
    elif(type=="otsu"):
        type=cv.THRESH_OTSU
    elif(type=="tozero"):
        type=cv.THRESH_TOZERO
    elif(type=="tozero inv"):
        type=cv.THRESH_TOZERO_INV

    e1 = cv.getTickCount()
    _,thresholdImage = cv.threshold(gray, 200, 255, type=cv.THRESH_TOZERO)
    e2 = cv.getTickCount()
    cv.imshow("2.1 - treshold tozero", thresholdImage)
    t = (e2 - e1)/cv.getTickFrequency()

    return thresholdImage, t

def edge(img, thresh1=100, thresh2=200):
    blured = img
    e1 = cv.getTickCount()
    edges = cv.Canny(blured,thresh1,thresh2)
    e2 = cv.getTickCount()
    t = (e2 - e1)/cv.getTickFrequency()
    cv.imshow("2.0.6 - canny detection", edges)

    return edges, t

def dilatation(img, type, size, iteration=1):
    edges = img
    kernel_size = size     #3,5,7 aua choix
    
    e1 = cv.getTickCount()
    if(type=="one"):
        kernel = np.ones((kernel_size,kernel_size),np.uint8)
    elif(type=="ellipse"):
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(kernel_size,kernel_size))
    elif(type=="cross"):
        kernel = cv.getStructuringElement(cv.MORPH_CROSS,(kernel_size,kernel_size))

    #erosion = cv.erode(edges,kernel,iterations = 1)
    dilatation = cv.dilate(edges, kernel, iteration)
    
    e2 = cv.getTickCount()
    t = (e2 - e1)/cv.getTickFrequency()

    cv.imshow("dilation", dilatation)

    return dilatation, t

def erosion(img, type, size, iteration=1):
    edges = img
    kernel_size = size     #3,5,7 aua choix
    
    e1 = cv.getTickCount()
    if(type=="one"):
        kernel = np.ones((kernel_size,kernel_size),np.uint8)
    elif(type=="ellipse"):
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(kernel_size,kernel_size))
    elif(type=="cross"):
        kernel = cv.getStructuringElement(cv.MORPH_CROSS,(kernel_size,kernel_size))

    erosion = cv.erode(edges,kernel,iterations = 1)
    
    e2 = cv.getTickCount()
    t = (e2 - e1)/cv.getTickFrequency()

    cv.imshow("Erosion", erosion)

    return erosion, t

def gray2rgb(img):
    blured_edges = img
    e1 = cv.getTickCount()
    couleur = cv.cvtColor(blured_edges, cv.COLOR_GRAY2RGB)
    e2 = cv.getTickCount()
    cv.imshow("toRGB", couleur)
    t = (e2 - e1)/cv.getTickFrequency()

    return couleur, t

def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):   
    e1 = cv.getTickCount() 
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
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        
        buf = cv.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    e2 = cv.getTickCount()
    t = (e2 - e1)/cv.getTickFrequency()
    cv.imshow("Brigtness constrast", buf)

    return buf,t

origin = loadImg()
img = crop(origin)
img, t = apply_brightness_contrast(img, -100,120)
print(t)
img, t = bgr2gray(img)
print(t)
# img,_ = GaussianBlur(img,3)
# img,_ = edge(img)
# img,_ = gray2rgb(img)


cv.waitKey()