from dis import dis
from xml import dom
import cv2 as cv
import sys
from cv2 import threshold
import numpy as np




def is_arrivee(name_image) :
    ##load imagesv
    origin = cv.imread(cv.samples.findFile(name_image))
    if origin is None:
        sys.exit("Could not read the image.")


    threshold_value = 120       #distance entre la couleur dominante detectée et la couleur target
    target_R = 239              #couleur RGB target
    target_G = 219
    target_B = 90

    y=97
    x=0
    h=25
    w=215
    crop_img = origin[y:y+h, x:x+w]

    ## dominant color detection

    a2D = crop_img.reshape(-1,crop_img.shape[-1])
    col_range = (256, 256, 256) # generically : a2D.max(0)+1
    a1D = np.ravel_multi_index(a2D.T, col_range)
    dom_color = np.unravel_index(np.bincount(a1D).argmax(), col_range)

    img_B = dom_color[0]
    img_G = dom_color[1]
    img_R = dom_color[2]

    distance = np.absolute(target_R - img_R) + np.absolute(target_G - img_G) + np.absolute(target_B - img_B)
    print(distance)


    yellow = False      #par defaut la ligne n'est pas detectée
    if(distance<threshold_value):
        yellow = True

    return yellow              #return true si la distance est assez petite, cela signifie que la couleur est detectée, donc que la ligne d'arrivée est devant

ok = "ok"
nop = "nop"
jpg = ".jpg"
arrivee = "_arrivee_"
txt=""
for i in range(1,10):
    if i<6:
        txt = str(i)+arrivee+nop+jpg
    else:
        txt = str(i-5)+arrivee+ok+jpg
    if txt!="":
        print(is_arrivee(txt))
        print("")


"1_arrivee_ok.jpg"








"""
##load imagesv
origin = cv.imread(cv.samples.findFile("1_arrivee_ok.jpg"))
if origin is None:
    sys.exit("Could not read the image.")


cv.imshow("0 - original", origin)


threshold_value = 120       #distance entre la couleur dominante detectée et la couleur target
target_R = 239              #couleur RGB target
target_G = 219
target_B = 90

y=97
x=0
h=25
w=215
crop_img = origin[y:y+h, x:x+w]
cv.imshow("0.1 -crop", crop_img)

#print(crop_img.shape)
## dominant color detection
e1 = cv.getTickCount()

a2D = crop_img.reshape(-1,crop_img.shape[-1])
col_range = (256, 256, 256) # generically : a2D.max(0)+1
a1D = np.ravel_multi_index(a2D.T, col_range)
dom_color = np.unravel_index(np.bincount(a1D).argmax(), col_range)

e2 = cv.getTickCount()
t = (e2 - e1)/cv.getTickFrequency()
print( "dominant color detection  : " ,t)


img_B = dom_color[0]
img_G = dom_color[1]
img_R = dom_color[2]

distance = np.absolute(target_R - img_R) + np.absolute(target_G - img_G) + np.absolute(target_B - img_B)
print(distance)


yellow = False      #par defaut la ligne n'est pas detectée
if(distance<threshold_value):
    yellow = True

print(yellow)
#return yellow              #return true si la distance est assez petite, cela signifie que la couleur est detectée, donc que la ligne d'arrivée est devant

"""