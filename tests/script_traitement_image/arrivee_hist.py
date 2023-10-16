import sys
import cv2 as cv
from matplotlib import pyplot as plt
import os, os.path
import numpy as np

# noYellow => il n'y a pas de yellow dans le dossier 
# => si il y a une erreur alors il a detecté du yellow alors qu'il ne devait pas en avoir

def loadImg(debug = True,
            nom = "9_arrivee_ok.jpg"):
    origin = cv.imread(cv.samples.findFile(nom))
    if origin is None:
        sys.exit("Could not read the image.")
    if(debug):
        cv.imshow("Original", origin)
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

def printHist(path = "C:\\Users\\ahdel\\projects\\enregistrement\\24_03\\images"):
    valid_images = [".jpg",".gif",".png",".tga"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        img = loadImg(os.path.join(path,f))
        img = crop(img)
        hist(img)

def erosion(img, type="one", size=5, iteration=3):
    edges = img
    kernel_size = size     #3,5,7 aua choix
    
    e1 = cv.getTickCount()
    if(type=="one"):
        kernel = np.ones((kernel_size,kernel_size),np.uint8)
    elif(type=="ellipse"):
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(kernel_size,kernel_size))
    elif(type=="cross"):
        kernel = cv.getStructuringElement(cv.MORPH_CROSS,(kernel_size,kernel_size))

    erosion = cv.erode(edges,kernel,iteration)
    
    e2 = cv.getTickCount()
    t = (e2 - e1)/cv.getTickFrequency()

    cv.imshow("Erosion", erosion)

    return erosion, t

def getLargeur(img):
    return len(img)

def getHauteur(img):
    return len(img[0])

def getNbPixel(img):
    return getLargeur(img)*getHauteur(img)

def hsvMask(img, debug = True ,HLow=0, HHigh=39, SLow=79, SHigh=255, VLow=123, VHigh=255):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    hsv_low  = np.array([HLow, SLow, VLow], np.uint8)
    hsv_high = np.array([HHigh, SHigh, VHigh], np.uint8)
    
    mask = cv.inRange(hsv, hsv_low, hsv_high)
    cuted = cv.bitwise_and(img, img, mask=mask)
    
    if(debug):
        cv.imshow("Mask", mask)
        cv.imshow("Cuted", cuted)
        print(getPercentagePixelWhite(mask))
        cv.waitKey(700)

    return mask, cuted

def yellow(debug = True,
            pathYellow = "C:\\Users\\ahdel\\projects\\enregistrement\\Yellow", ):
    valid_images = [".jpg",".gif",".png",".tga"]
    masks = []
    cuteds = []
    imgs = []
    for f in os.listdir(pathYellow):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        img = loadImg(debug, os.path.join(pathYellow,f))
        # img = crop(img)
        mask, cuted = hsvMask(img, debug)
        masks.append(mask)
        cuteds.append(cuted)
        imgs.append(img)
    return masks, cuteds, imgs

def getPercentagePixelWhite(img):
    return (cv.countNonZero(img)*100)/getNbPixel(img)

def testYellow(threshold = 3, debug = False):
    masks, cuted, origin = yellow(debug)
    nbFail=0
    for i in range(len(masks)):
        print(getPercentagePixelWhite(masks[i]))
        if(getPercentagePixelWhite(masks[i])<threshold):
            print("Il n'y a pas de jaune, il n'aurait pas du en detecter")
            cv.imshow("Original", origin[i])
            cv.imshow("Cuted", cuted[i])
            cv.imshow("mask", masks[i])
            cv.waitKey(0)
            nbFail +=1
    print("Nb fail : "+str(nbFail)+ " over : "+str(len(masks)))
    return (nbFail*100)/len(masks)

def testNoYellow(threshold = 5, debug = False):
    masks, cuted, origin = yellow(debug, pathYellow= "C:\\Users\\ahdel\\projects\\enregistrement\\noYellow")
    nbFail=0
    for i in range(len(masks)):
        if(getPercentagePixelWhite(masks[i])>threshold):
            print("Il y a du jaune, il n'aurait pas du le detecter")
            cv.imshow("Original", origin[i])
            cv.imshow("Cuted", cuted[i])
            cv.imshow("mask", masks[i])
            cv.waitKey(0)
            nbFail +=1
    print("Nb fail : "+str(nbFail)+ " over : "+str(len(masks)))
    return (nbFail*100)/len(masks)

def green(debug = True,
            pathGreen = "C:\\Users\\ahdel\\projects\\enregistrement\\images"):
    valid_images = [".jpg",".gif",".png",".tga"]
    masks = []
    cuteds = []
    imgs = []
    for f in os.listdir(pathGreen):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        img = loadImg(debug, os.path.join(pathGreen,f))
        # img = crop(img)
        mask, cuted = hsvMask(img, debug, HLow=37, HHigh=103, SLow=111, SHigh=255, VLow=152, VHigh=255)
        masks.append(mask)
        cuteds.append(cuted)
        imgs.append(img)
    return masks, cuteds, imgs

def testGreen(threshold = 0.25, debug = False):
    masks, cuted, origin = green(debug)
    nbFail=0
    for i in range(len(masks)):
        print("Il n'y a pas de vert, il n'aurait pas du en detecter")
        cv.imshow("Original", origin[i])
        cv.imshow("Cuted", cuted[i])
        cv.imshow("mask", masks[i])
        cv.waitKey(0)
        nbFail +=1
    print("Nb fail green : "+str(nbFail)+ " over : "+str(len(masks)))
    return (nbFail*100)/len(masks)

def testNoGreen(threshold = 0.25, debug = False):
    masks, cuted, origin = green(debug, pathGreen = "C:\\Users\\ahdel\\projects\\enregistrement\\noGreen")
    nbFail=0
    for i in range(len(masks)):
        print("Il y a du vert, il n'aurait pas du le detecter")
        cv.imshow("Original", origin[i])
        cv.imshow("Cuted", cuted[i])
        cv.imshow("mask", masks[i])
        cv.waitKey(0)
        nbFail +=1
    print("Nb fail green : "+str(nbFail) + " over : "+str(len(masks)))
    return (nbFail*100)/len(masks)

def printResultatTests():
    # print("testYellow")
    # percentageFailTestYellow = testYellow()

    # print("testNoYellow")
    # percentageFailTestNoYellow = testNoYellow()

    print("testGreen")
    percentageFailtestGreen = testGreen()

    # print("testYellow")
    # percentageFailtestNoGreen = testNoGreen()

    print("Resultat tests")
    # print("testYellow : "+str(percentageFailTestYellow))
    # print("testNoYellow : "+str(percentageFailTestNoYellow))
    print("testGreen : "+str(percentageFailtestGreen))
    # print("testNoGreen : "+str(percentageFailtestNoGreen))

    print("Il y a beaucoup d'erreur dans yellow et green car le treshold limite les image non conformes (genre ligne trop loin), aussi il y a beaucoup moins de photo dans yellow et green que dans noYellow et noGreen")

printResultatTests()