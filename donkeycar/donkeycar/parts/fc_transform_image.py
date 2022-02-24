#F&C Image transformation part
import numpy as np
import cv2
import time
import random
import collections
from PIL import Image, ImageDraw
import os
import urllib.request
from donkeycar.utils import *



class FC_TransformImage(object):

    def __init__(self, cfg, debug=False):
        self.debug = debug
        self.cfg = cfg
        self.trapezoidal_mask = None
        self.fcsetting = ":"
        print("F&C : Image transformation part activated.")


    def run(self, image, fcsetting=None, testValue1=None, testValue2=None):
        if image is None or image[0] is None:
            return image

        # Change setting from web controller input
        if not (fcsetting is None or fcsetting == ":" or fcsetting == "undefined:undefined"):
            self.fcsetting = fcsetting
            newsettingname,newsettingvalue = fcsetting.split(":")
            if ("TRANSFORM_IMAGE" in newsettingname):
                self.cfg.__setattr__(newsettingname,float(newsettingvalue))

        #F&C - Debug
        # Debug can be used as part of augment test script, with sliders.
        # Use testValue1 or 2 to pass values from sliders, and overide transformation config values.
        if self.debug:
            if testValue1 is not None:
                variable1 = testValue1
                pass
            else:
                variable1 = 0

            if testValue2 is not None:
                variable2 = testValue2
                pass
            else:
                variable2 = 0


        image = image.copy()
        originalimage = image
        

        #F&C - Get image dimensions for future usage :
        imageHeight, imageWidth, imageColorDepth = image.shape

        
        #F&C - Create mask if it does not already exists
        if self.trapezoidal_mask is None:
            self.trapezoidal_mask = np.zeros(image.shape, dtype=np.int32)
            # # # # # # # # # # # # #
            #       ul     ur          min_y
            #
            #
            #
            #    ll             lr     max_y

            # Variables order
            #[upper_left, min_y],
            #[upper_right, min_y],
            #[lower_right, max_y],
            #[lower_left, max_y]
            points = [
                [imageWidth*self.cfg.TRANSFORM_IMAGE_CROP_TOP_SIDE/100, imageHeight*self.cfg.TRANSFORM_IMAGE_CROP_TOP/100],
                [imageWidth-(imageWidth*self.cfg.TRANSFORM_IMAGE_CROP_TOP_SIDE/100), imageHeight*self.cfg.TRANSFORM_IMAGE_CROP_TOP/100],
                [imageWidth-(imageWidth*self.cfg.TRANSFORM_IMAGE_CROP_BOTTOM_SIDE/100), imageHeight-(imageHeight*self.cfg.TRANSFORM_IMAGE_CROP_BOTTOM/100)],
                [imageWidth*self.cfg.TRANSFORM_IMAGE_CROP_BOTTOM_SIDE/100, imageHeight-(imageHeight*self.cfg.TRANSFORM_IMAGE_CROP_BOTTOM/100)]
            ]
            cv2.fillConvexPoly(self.trapezoidal_mask, np.array(points, dtype=np.int32),
                                [255, 255, 255])
            self.trapezoidal_mask = np.asarray(self.trapezoidal_mask, dtype='bool')

        
        #F&C - Apply mask at the begining (useless)
        image = np.multiply(image, self.trapezoidal_mask)

        #F&C - Crop top images
        if(self.cfg.TRANSFORM_IMAGE_CROP_RESIZE):
            image = image[int(imageHeight*self.cfg.TRANSFORM_IMAGE_CROP_TOP/100):int(imageHeight-(imageHeight*self.cfg.TRANSFORM_IMAGE_CROP_BOTTOM/100)), 0:imageWidth]


        #F&C - Remove high luminosity glares and details
        lumSoftThreshold = self.cfg.TRANSFORM_IMAGE_SOFT_THRESHOLD_LUM
        lumHardThreshold = self.cfg.TRANSFORM_IMAGE_HARD_THRESHOLD_LUM
        satHardThreshold = self.cfg.TRANSFORM_IMAGE_HARD_THRESHOLD_SAT

        #Debug
        #lumSoftThreshold = variable1+1
        #satHardThreshold = variable1
        #lumHardThreshold = variable2

        if(lumSoftThreshold < 255) or (lumHardThreshold < 255):
            #Convert image to HSV
            image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hue,sat,val = cv2.split(image_HSV)
            factor = float(255/lumSoftThreshold)

            #Hard Threshold :  
            #Removing high luminosity glares by considering pixels with high luminosity (value) and low saturation. The value is set to the middle luminosity value.
            val = np.where((val >= lumHardThreshold) & (sat <= satHardThreshold),lumHardThreshold/2,val)

            #Soft Threshold :
            #Limit pixels where value is over threshold
            val = np.where((val >= lumSoftThreshold), lumSoftThreshold ,val)

            
            #Straighten out luminosity :
            val = (val * factor)                         
            
            val = val.astype(np.uint8)
            #Convert back to BGR
            image_HSV = cv2.merge([hue, sat, val])
            image = cv2.cvtColor(image_HSV, cv2.COLOR_HSV2BGR)
            
        
        #F&C - Contrast and brightness
        if (not self.cfg.TRANSFORM_IMAGE_BRIGHTNESS == 0) or (not self.cfg.TRANSFORM_IMAGE_CONTRAST == 0):
            image = self.apply_brightness_contrast(image, self.cfg.TRANSFORM_IMAGE_BRIGHTNESS, self.cfg.TRANSFORM_IMAGE_CONTRAST)
        
        #Debug : 
        #image = self.apply_brightness_contrast(image, variable1, variable2)
        

        #F&C - Remove details -- Too slow
        #image = cv2.edgePreservingFilter(image, flags=1, sigma_s=self.cfg.TRANSFORM_IMAGE_EDGE_SIZE, sigma_r=self.cfg.TRANSFORM_IMAGE_EDGE_COLOR/100)

        #F&C - Blur (useless)
        #kernel_size = 5
        #image = cv2.GaussianBlur(image,(kernel_size, kernel_size),0)


        #F&C - Revert image (negative)
        if(self.cfg.TRANSFORM_IMAGE_REVERSE):
            image = cv2.bitwise_not(image)


        #F&C - Adding Laplacian filtering
        if(self.cfg.TRANSFORM_IMAGE_BORDERS and self.cfg.TRANSFORM_IMAGE_BORDERS_WEIGHT > 0.0):
            #Applying a mask to filter pixels used in border detection (helps to remove noise)
            sourceImagesBordersHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            mask_min_lum = self.cfg.TRANSFORM_IMAGE_BORDERS_MIN_LUM
            mask_max_sat = self.cfg.TRANSFORM_IMAGE_BORDERS_MAX_SAT       

            #Debug :
            #mask_min_lum = variable1
            #mask_max_sat = variable2

            #White only mask :
            sourceImagesBordersMask = cv2.inRange(sourceImagesBordersHSV, (0, 0, mask_min_lum), (255, mask_max_sat ,255))

            #REMOVE
            #Remove yellow mask :
            if(self.cfg.TRANSFORM_IMAGE_BORDERS_FILTER_COLOR):
                sourceImagesBordersMaskNegative1 = 255-(cv2.inRange(sourceImagesBordersHSV, (35, 0, mask_min_lum), (120, mask_max_sat ,255)))
                sourceImagesBordersMask = cv2.bitwise_and(sourceImagesBordersMask, sourceImagesBordersMaskNegative1)

            #ADD
            #Alternative with multiple masks if necessary to include multiple colors :
            #sourceImagesBordersMask1 = sourceImagesBordersHSV.inRange(hsv, (36, 0, 0), (70, 255,255) #Color 1
            #sourceImagesBordersMask2 = sourceImagesBordersHSV.inRange(hsv, (15, 0, 0), (36, 255,255) #Color 1
            #sourceImagesBordersMask = cv2.bitwise_or(sourceImagesBordersMask1, sourceImagesBordersMask2)

            sourceImagesBordersHSV = cv2.bitwise_and(sourceImagesBordersHSV,sourceImagesBordersHSV, mask=sourceImagesBordersMask)

            sourceImageBorders = cv2.cvtColor(sourceImagesBordersHSV, cv2.COLOR_HSV2BGR)
            sourceImageBordersGray = cv2.cvtColor(sourceImageBorders, cv2.COLOR_BGR2GRAY)

            
            #sourceImageBordersMask = cv2.inRange(imageGray, self.cfg.TRANSFORM_IMAGE_BORDERS_MIN_LUM, 255)
            #sourceImageBorders =cv2.bitwise_and(imageGray, sourceImageBordersMask)

            #Apply Laplacian filter on grayscale image
            bordersImage = cv2.convertScaleAbs(cv2.Laplacian(sourceImageBordersGray, cv2.CV_16S, ksize=3))

            #Converts back to BGR
            bordersImage = cv2.cvtColor(bordersImage, cv2.COLOR_GRAY2BGR)
            
            #Debug : Show mask as output
            #bordersImage = cv2.cvtColor(sourceImagesBordersMask, cv2.COLOR_GRAY2BGR)

            #Enhance borders contrast to remove noise
            contrast = 20
            f = float(131 * (contrast + 127)) / (127 * (131 - contrast))
            alpha_c = f
            gamma_c = 127*(1-f)
            bordersImage = cv2.addWeighted(bordersImage, alpha_c, bordersImage, 0, gamma_c)

            #Crop top borders image
            bordersImage[:int(imageHeight/100*self.cfg.TRANSFORM_IMAGE_BORDERS_CROP_TOP)  ,  :  ,  :  ] = 0


        #F&C - Use grayscale image
        if(self.cfg.TRANSFORM_IMAGE_GRAYSCALE):
            
            #F&C - Converting to grayscale
            imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.cvtColor(imageGray, cv2.COLOR_GRAY2BGR)


        #Line detection
        # rho = 1  # distance resolution in pixels of the Hough grid
        # theta = np.pi / 180  # angular resolution in radians of the Hough grid
        # threshold = 50  # minimum number of votes (intersections in Hough grid cell)
        # min_line_length = 80  # minimum number of pixels making up a line
        # max_line_gap = 2  # maximum gap in pixels between connectable line segments
        # line_image = np.copy(image) * 0  # creating a blank to draw lines on

        # # Run Hough on edge detected image
        # # Output "lines" is an array containing endpoints of detected line segments
        # lines = cv2.HoughLinesP(cv2.cvtColor(bordersImage, cv2.COLOR_BGR2GRAY), rho, theta, threshold, np.array([]),
        #                     min_line_length, max_line_gap)

        # if not lines is None:
        #     for line in lines:
        #         for x1,y1,x2,y2 in line:
        #             cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),2)


        #F&C - Combine original image and borders
        if(self.cfg.TRANSFORM_IMAGE_BORDERS and self.cfg.TRANSFORM_IMAGE_BORDERS_WEIGHT > 0.0):
            image = cv2.addWeighted(image, self.cfg.TRANSFORM_IMAGE_ORIGINAL_WEIGHT, bordersImage, self.cfg.TRANSFORM_IMAGE_BORDERS_WEIGHT, 0.0)
 
        return image

    def apply_brightness_contrast(self, input_img, brightness = 255, contrast = 127):
        #Source : https://www.life2coding.com/change-brightness-and-contrast-of-images-using-opencv-python/
        #brightness = map(brightness, 0, 510, -255, 255)
        #contrast = map(contrast, 0, 254, -127, 127)
        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + brightness
            alpha_b = (highlight - shadow)/255
            gamma_b = shadow
            buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
        else:
            buf = input_img.copy()
        if contrast != 0:
            f = float(131 * (contrast + 127)) / (127 * (131 - contrast))
            alpha_c = f
            gamma_c = 127*(1-f)
            buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
        
        return buf

    
