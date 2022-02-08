#F&C Race management part
import numpy as np
import cv2
import time
import random
import collections
import os
import urllib.request

class FC_RaceManager(object):

    def __init__(self, cfg):
        self.raceStarted = False
        self.raceFinished = False
        self.raceAllowReset = False
        self.cfg = cfg
        self.green_light_threshold = cfg.RACE_M_GREEN_THRESHOLD
        self.yellow_line_threshold = cfg.RACE_M_YELLOW_THRESHOLD
        self.maxLaps = cfg.RACE_M_MAX_LAPS
        self.currentLap = 0
        self.bestLapTime = None
        self.detection_time_thrshold = 10 # Time in secs between each yellow line detection
        self.yellow_line_detected = False
        print("F&C : Race Management part activated.")


    def run(self, img_arr, mode, fc_messages, fcsetting=None):
        if img_arr is None or img_arr[0] is None:
            return img_arr, mode, fc_messages, self.currentLap

        # Change setting from web controller input
        if not (fcsetting is None or fcsetting == ":" or fcsetting == "undefined:undefined"):
            self.fcsetting = fcsetting
            newsettingname,newsettingvalue = fcsetting.split(":")
            if ("RACE_M" in newsettingname):
                newsettingvalue = eval(newsettingvalue)
                self.cfg.__setattr__(newsettingname,newsettingvalue)

        img_arr_original = img_arr
        

        # Race is started : ignore mode change
        if(self.raceStarted):
            mode = "local"
            self.raceAllowReset = False

            # Ignore line detection if already detect recently
            if (time.time() - self.last_yellow_line_detection_time > self.detection_time_thrshold):
                _,result = self.detect_yellow_line(img_arr)
            
                if(result > self.yellow_line_threshold): # Numbers of pixel to validate yellow light
                    print("F&C : Yellow line detected !")
                    self.yellow_line_detected = True

                else:
                    if self.yellow_line_detected: # Yellow line is no longer detected. Counting a new lap.
                        self.yellow_line_detected = False
                        self.last_yellow_line_detection_time = time.time()
                        # Calculate lap time
                        self.lapEndTime = time.time()
                        self.lastLapTime = round((self.lapEndTime - self.lapBeginTime),2)

                        if (self.bestLapTime is None):
                            self.bestLapTime = self.lastLapTime
                            fc_messages.append("New lap (" + str(self.currentLap) + ") : " + str(self.lastLapTime) + " secs")
                        elif (self.lastLapTime < self.bestLapTime):
                            self.bestLapTime = self.lastLapTime
                            fc_messages.append("New lap (" + str(self.currentLap) + ") : " + str(self.lastLapTime) + " secs - NEW LAP RECORD !")
                        else:
                            fc_messages.append("New lap (" + str(self.currentLap) + ") : " + str(self.lastLapTime) + " secs (+" + str(round((self.lastLapTime - self.bestLapTime),2)) + " secs)")

                        self.currentLap += 1
                        self.lapBeginTime = time.time()

                    
            # Stop when race is complete
            if (self.currentLap > self.maxLaps):
                print("F&C : END OF RACE detected !")
                fc_messages.append("END OF RACE ! Best lap time : " + str(self.bestLapTime) + " secs")
                self.raceAllowReset = True
                self.raceFinished = True
                self.raceStarted = False
                self.currentLap = self.maxLaps

        # Race is over : Waiting for reset
        elif(self.raceFinished):
            if(mode == 'user'):
                if (self.raceAllowReset):
                    self.raceStarted = False
                    self.raceFinished = False
                    self.raceAllowReset = False
                    self.currentLap = 0
                    self.bestLapTime = None
                    fc_messages.append("Race mode reseted. Ready !")
            else:
                mode == 'waiting'

        # Waiting for race to begin
        else:
            #Waiting mode
            if(mode == 'waiting'):
                # Detect traffic light object
                img_arr,result = self.detect_green_traffic(img_arr)

                # If green light is found, switch to auto driving mode:
                if(result > self.green_light_threshold): # Numbers of pixel to validate green light
                    self.raceStarted = True
                    self.lapBeginTime = time.time()
                    self.last_yellow_line_detection_time = time.time()
                    self.yellow_line_detected = False
                    self.currentLap = 1

                    outputString = "\n"
                    outputString += "+-=============================================-+\n"
                    outputString += " >>>>             green light !             <<<<\n"
                    outputString += " >>>>                                       <<<<\n"
                    outputString += " >>>>  FAST & CURIOUS  :  STARTING RACE !!  <<<<\n"
                    outputString += " >>>>                                       <<<<\n"
                    outputString += "+-=============================================-+\n"
                    outputString += "\n"
                    print(outputString)
                    mode = "local"
                    fc_messages.append("Green light detected, STARTING RACE !")
                    print("F&C : Green light detected !")

                else:
                    mode = "waiting"
                    #Only add message once
                    if not (fc_messages[-1] == "Waiting for green light..."):
                        print("F&C : waiting for Green light...")
                        fc_messages.append("Waiting for green light...")
            
            elif(mode == 'waiting_test'):
                img_arr_top,_ = self.detect_green_traffic(img_arr)
                img_arr_bottom,_ = self.detect_yellow_line(img_arr)
                
                # Stack green light and yellow light detection results
                height, _, _ = img_arr.shape
                img_arr_top = img_arr_top.copy()
                img_arr_top = img_arr_top[:int(height/2),  :  ,  :  ]
                img_arr_bottom = img_arr_bottom.copy()
                img_arr_bottom = img_arr_bottom[int(height/2):,  :  ]
                img_arr = np.vstack((img_arr_top,img_arr_bottom))

                #Only add message once
                if not (fc_messages[-1] == "Testing detection..."):
                    fc_messages.append("Testing detection...")

        return img_arr, mode, fc_messages, self.currentLap


    # F&C : Green traffic light detection
    def detect_green_traffic(self, img_arr):
        #img_arr = self.apply_brightness_contrast(img_arr, -40, 0)

        # Crop bottom pixels
        img_arr = img_arr.copy()
        height, _, _ = img_arr.shape
        img_arr[int(height/4):  ,  :  ,  :  ] = 0

        originalimage = img_arr
        hsv = cv2.cvtColor(img_arr, cv2.COLOR_BGR2HSV)

        # Enhance saturation :
        #hue,sat,val = cv2.split(hsv)
        #sat = sat
        #sat = np.where((sat > 255), 255 , sat)
        #hsv = cv2.merge([hue, sat, val])
        #img_arr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        lower_green = np.array([self.cfg.RACE_M_GREEN[0]])
        upper_green = np.array([self.cfg.RACE_M_GREEN[1]])

        mask = cv2.inRange(hsv, lower_green, upper_green)
        res = cv2.bitwise_and(img_arr, img_arr, mask = mask)

        grey = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        # applying gaussian blur
        value = (35, 35)
        blurred = cv2.GaussianBlur(grey, value, 0)

        _, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        thresh = cv2.bitwise_not(thresh1)
        value = np.count_nonzero(thresh)

        thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        thresh[:,:,0] = np.zeros([thresh.shape[0], thresh.shape[1]])
        thresh[:,:,2] = np.zeros([thresh.shape[0], thresh.shape[1]]) # Only keep green channel
        image = cv2.addWeighted(originalimage, 0.9, thresh, 0.5, 0.0)

        image = cv2.putText(
            image,
            str(value) + "<" + str(self.green_light_threshold),
            (10,int(height/3+20)), #Position
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, #font size
            (0, 255, 0), #font color
            2) #font thickness

        return image, value


    def detect_yellow_line(self, img_arr):
        #img_arr = self.apply_brightness_contrast(img_arr, -40, 0)

        # Crop top pixels
        img_arr = img_arr.copy()
        height, _, _ = img_arr.shape
        img_arr[:int(height-height/4),  :  ,  :  ] = 0

        originalimage = img_arr
        hsv = cv2.cvtColor(img_arr, cv2.COLOR_BGR2HSV)

        # Enhance saturation :
        #hue,sat,val = cv2.split(hsv)
        #sat = sat
        #sat = np.where((sat > 255), 255 , sat)
        #hsv = cv2.merge([hue, sat, val])
        #img_arr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        lower_yellow = np.array([self.cfg.RACE_M_YELLOW[0]])
        upper_yellow = np.array([self.cfg.RACE_M_YELLOW[1]])

        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        res = cv2.bitwise_and(img_arr, img_arr, mask = mask)

        grey = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        # applying gaussian blur - Disabled (seems useless, an use ~2Hz)
        #value = (5, 5)
        #blurred = grey
        #blurred = cv2.GaussianBlur(grey, value, 0)

        _, thresh1 = cv2.threshold(grey, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        thresh = cv2.bitwise_not(thresh1)
        value = np.count_nonzero(thresh)

        thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        thresh[:,:,0] = np.zeros([thresh.shape[0], thresh.shape[1]])
        #thresh[:,:,1] = np.zeros([thresh.shape[0], thresh.shape[1]]) # Only keep one channel
        image = cv2.addWeighted(originalimage, 0.9, thresh, 0.5, 0.0)

        image = cv2.putText(
            image,
            str(value) + "<" + str(self.yellow_line_threshold),
            (10,int(height-(height/4)-20)), #Position
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, #font size
            (255, 255, 0), #font color
            2) #font thickness

        return image, value


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
