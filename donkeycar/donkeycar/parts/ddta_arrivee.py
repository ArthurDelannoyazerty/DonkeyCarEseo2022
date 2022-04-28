import cv2 as cv
import numpy as np

class DDTA_CvImage(object):

    def __init__(self):
        print("DDTA : Arrivee Part activated")


    def run(self, image):
        if image is None or image[0] is None:
            return image
        
        image = image.copy()
        originalimage = image
        
        threshold_value = 120       #distance entre la couleur dominante detectée et la couleur target
        target_R = 239              #couleur RGB target
        target_G = 219
        target_B = 90

        y=97
        x=0
        h=25
        w=215

        crop_img = image[y:y+h, x:x+w]
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
        

        
        return yellow