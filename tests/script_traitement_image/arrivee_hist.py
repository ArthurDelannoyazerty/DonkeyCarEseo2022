import sys
from time import sleep
import cv2 as cv
from matplotlib import pyplot as plt

def loadImg(nom = "circuit_normal1.jpg"):
    origin = cv.imread(cv.samples.findFile(nom))
    if origin is None:
        sys.exit("Could not read the image.")
    cv.imshow("0 - original", origin)
    return origin

def crop(img,x=50,y=60,h=65,w=61):
    origin = img
    crop_img = origin[y:y+h, x:x+w]
    cv.imshow("Crop", crop_img)
    return crop_img

def hist(img):
    isYellow = False
    color = ('b','g','r')
    arrayColorRandom=[]     #[B1,B2,G1,G2,R1,R2] -> peut etre g et R inversé ici
    pixelValue1 = 170
    pixelValue2 = 180
    for i,col in enumerate(color):
        e1 = cv.getTickCount()
        histr = cv.calcHist([img],[i],None,[256],[0,256])
        arrayColorRandom.append(histr[pixelValue1][0])
        arrayColorRandom.append(histr[pixelValue2][0])
        
        e2 = cv.getTickCount()
        t = (e2 - e1)/cv.getTickFrequency()
        plt.plot(histr,color = col)
        plt.xlim([0,256])
    print(arrayColorRandom)
    if(arrayColorRandom[4]!=0 and 
       arrayColorRandom[5]!=0 and
       arrayColorRandom[2]!=0 and
       arrayColorRandom[3]!=0 and
       arrayColorRandom[0]<2 and
       arrayColorRandom[1]<2):
       isYellow = True
       print("YELOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOW")
    plt.show(block=False)
    plt.pause(0.3)
    plt.close()
    return isYellow

# img = loadImg()
# img = crop(img)
# hist(img)
# print("1")

# img = loadImg("5_arrivee_nop.jpg")
# img = crop(img)
# hist(img)
# img = loadImg("6_arrivee_nop.jpg")
# img = crop(img)
# hist(img)

from PIL import Image
import os, os.path

imgs = []
path = "C:\\Users\\ahdel\\projects\\enregistrement\\24_03\\images"
valid_images = [".jpg",".gif",".png",".tga"]
for f in os.listdir(path):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    img = loadImg(os.path.join(path,f))
    img = crop(img)
    hist(img)




"""
ok = "ok"
nop = "nop"
jpg = ".jpg"
arrivee = "_arrivee_"
txt=""
for i in range(1,10):
    if i<7:
        txt = str(i)+arrivee+nop+jpg
    else:
        txt = str(i-5)+arrivee+ok+jpg
    if txt!="":
        img = loadImg(txt)
        img = crop(img)
        hist(img)
        print("")
"""


# cv.waitKey()