#F&C Information part
import time
import psutil
from PIL import Image, ImageDraw
from prettytable import PrettyTable
import numpy as np
import cv2
import math
import os


class FC_Information(object):

    def __init__(self, frequency, showconsole):
        self.deg_to_rad = math.pi / 180.0
        self.frequency = frequency
        self.showconsole = showconsole
        self.runs_counter = 1
        self._on = True
        self.starting = True
        self.last_calc_time = time.time()-1 # -1 is to avoid /0 error in some condition
        self.last_calc_time_warning = time.time()-1 # -1 is to avoid /0 error in some condition
        self.last_update_time = time.time()-1 # -1 is to avoid /0 error in some condition
        self.last_display_time = time.time()-1 # -1 is to avoid /0 error in some condition
        self.angle = 0
        self.throttle = 0
        self.records = 0
        self.recording = False
        self.previousio = round(psutil.disk_io_counters()[0] + psutil.disk_io_counters()[1])
        self.mode = "starting"
        self.information = ""
        self.pilImage = None
        self.imageWidth = 160
        self.textImageOutput = None
        self.fc_messages = ["","",""]
        self.fc_multiplier = 1.0
        self.battery = 0.0
        self.voltage = 0.0
        self.outputimage = None
        try:
            self.pimode = os.uname()[4].startswith("arm") 
        except:
            self.pimode = False

        if self.pimode: # Detecting I2C addresses
            from donkeycar.management.ina219 import INA219
                
            adress = os.popen("i2cdetect -y -r 1 0x41 0x41 | egrep '41' | awk '{print $2}'").read()
            if(adress=='41\n'):
                self.ina219 = INA219(addr=0x41)
            else:
                self.ina219 = None

            adress = os.popen("i2cdetect -y -r 1 0x42 0x42 | egrep '42' | awk '{print $2}'").read()
            if(adress=='42\n'):
                self.ina = INA219(addr=0x42)
            else:
                self.ina = None
            print("F&C : Information part activated in PI mode.")

        else:
            print("F&C : Information part activated.")
        self.update_metrics()


    # Update system metrics
    def update_metrics(self):
        
        
        # Don't update system part at all cycles to reduce CPU usage
        if ((time.time()-self.last_update_time) > self.frequency):
            self.car_frequency = self.runs_counter/(time.time()-self.last_calc_time)
            self.runs_counter = 1
            self.last_calc_time = time.time()-0.001 # Removing a ms to avoid /0

            self.mem_percent = psutil.virtual_memory().percent
            self.cpu_percent = psutil.cpu_percent()
            self.cpu_freq = psutil.cpu_freq().current
            
            self.io = round(psutil.disk_io_counters()[0] + psutil.disk_io_counters()[1]) - self.previousio
            self.previousio = round(psutil.disk_io_counters()[0] + psutil.disk_io_counters()[1])
            self.iops = round(self.io / (time.time()-self.last_update_time))

            self.recordingState = " "
            if self.recording:
                self.recordingState = "*"

            if self.pimode:
                if(self.ina != None):
                    self.voltage = self.ina.getBusVoltage_V()        # voltage on V- (load side)
                    self.battery = (self.voltage - 6)/2.4*100
                    self.voltage = self.voltage - 7.4 # Show relative voltage
                elif(self.ina219 != None):
                    self.voltage = self.ina219.getBusVoltage_V()        # voltage on V- (load side)
                    self.battery = (self.voltage - 9)/3.6*100
                    self.voltage = self.voltage - 12.6 # Show relative voltage
                elif(self.ads != None):
                    value=self.ads.readVoltage(4)/1000.0
                    self.battery = value/12.6*100
                
                if(self.battery > 100):self.battery = 100
                if(self.battery < 0):self.battery = 0

            self.last_update_time = time.time()-0.001 # Removing a ms to avoid /0

        

    # Update part, which only runs at the defined frequency (to avoid a performance drop)
    def update(self):
        while self._on:
            if self.starting:
                time.sleep(5) # Waiting for startup
                self.starting = False

            self.update_metrics()

            outputString = "\nStarting..."

            if not (self.starting):
                outputString = "\n"

                if self.pimode:
                    outputString += ("+-----------------------+-----------+-----------+\n")
                    outputString += ("|                       | BAT:" + self.fixedWidth(round(self.battery),3) + "%  | VLT:" + self.fixedWidth(round(self.voltage,1),4) + "V |\n")

                outputString += ("+-----------------------+-----------+-----------+\n")
                #     "| CPU:xx.x% | MEM:xx.x% | FRE:xx Hz | "
                outputString += ("| CPU:" + self.fixedWidth(self.cpu_percent,5) + "% (" + self.fixedWidth(round(self.cpu_freq),4) + " GHz) | MEM:" + self.fixedWidth(self.mem_percent,4) + "% | DIO:" + self.fixedWidth(self.iops,5) + " |\n")
                outputString += ("+-----------------------+-----------+-----------+\n")
                outputString += ("| THR:" + self.fixedWidth(round(self.throttle,2),5) + "(MULT=x" + self.fixedWidth(round(self.fc_multiplier,2),4) + ") | ANG:" + self.fixedWidth(round(self.angle,2),6) + "| FRQ:" + self.fixedWidth(round(self.car_frequency),3) + "Hz |\n")
                outputString += ("+-----------------------+-----------+-----------+\n")
                outputString += ("| TCACT: " + self.fixedWidth(self.fc_currentthrottle_info.type,12) + "   | " + self.fixedWidth(self.fc_currentthrottle_info.action,5) +"     | " + self.fixedWidth(self.fc_currentthrottle_info.multiplicator,6) + "    |\n")
                outputString += ("+-----------------------+-----------+-----------+\n")
                outputString += ("| MOD: " + self.fixedWidth(self.mode,12) + "     | LAP:" + self.fixedWidth(self.fc_current_lap,2) +"    |" + self.recordingState + "REC:" + self.fixedWidth(self.records,5) + self.recordingState + "|\n")
                outputString += ("+-----------------------+-----------+-----------+\n")
                outputString += ("| " + self.fixedWidth(self.fc_messages[-3],45) + " |\n")
                outputString += ("| " + self.fixedWidth(self.fc_messages[-2],45) + " |\n")
                outputString += ("| " + self.fixedWidth(self.fc_messages[-1],45) + " |\n")
                outputString += ("+-----------------------------------------------+\n\n")
            
            self.information = outputString

            if (self.showconsole):
                if ((time.time()-self.last_display_time) > self.frequency):
                    print(self.information) # Show information to console
                    self.last_display_time = time.time()-0.001 # Removing a ms to avoid /0


            #Generates output image
            if not (self.starting):
                self.transformedimage = self.transformedimage.copy()
                self.transformedimage = self.draw_user_input_fc(self.transformedimage)

            #Stack original image and transformed image
            imageHeight, imageWidth, imageColorDepth = self.originalimage.shape
            image2Height, image2Width, image2ColorDepth = self.transformedimage.shape
            transformedimageExp = np.zeros((imageHeight, imageWidth, 3), np.uint8)
            transformedimageExp[:] = (255,255,255)
            transformedimageExp[0:image2Height,0:image2Width] = self.transformedimage
            self.webimage = np.hstack((self.originalimage,transformedimageExp))
            _, self.imageWidth, _ = self.webimage.shape


            #Generate image from text
            self.pilImage = Image.new('RGB', (self.imageWidth, 150), color = (255, 255, 255))

            d = ImageDraw.Draw(self.pilImage)
            y0, dy = 0, 9
            for i, line in enumerate(self.information.split('\n')):
                y = y0 + i*dy
                d.text((9,y), line, fill=(0,0,0))

            self.textImageOutput = np.array(self.pilImage)


            #Stack images with information output
            if not (self.textImageOutput is None):
                self.outputimage = np.vstack((self.webimage,self.textImageOutput))
            else:
                self.outputimage = self.webimage

            time.sleep(0.05) # Frequency used to refresh image.


    def shutdown(self):
        self._on = False
        print('F&C : Stopping information part.')
        time.sleep(0.5)


    # Main update loop, used to stack images
    def run_threaded(self, angle, throttle, records, mode, recording, transformedimage, originalimage, fc_messages, fc_multiplier, fc_current_lap, fc_currentthrottle_info):
        self.runs_counter += 1
        self.angle = angle
        self.throttle = throttle
        self.records = records
        self.mode = mode
        self.recording = recording
        self.fc_multiplier = fc_multiplier
        self.fc_current_lap = fc_current_lap
        self.fc_currentthrottle_info = fc_currentthrottle_info
        self.fc_messages = fc_messages
        self.transformedimage = transformedimage
        self.originalimage = originalimage

        if (originalimage is None) or (transformedimage is None) or (self.starting) or (self.outputimage is None):
            return self.information,originalimage, self.battery       
        
        
        # Displays a warning message if a cycle is below a threshold
        self.car_frequency_warning = 1/(time.time()-self.last_calc_time_warning)
        self.last_calc_time_warning = time.time()-0.001 # Removing a ms to avoid /0
       
        #Debug :
        if (self.car_frequency_warning < 10):
            print("/!\ LOW FREQUENCY : " + str(round(self.car_frequency_warning,3)) + " Hz")
        #Debug :
        #else:
            #print("    " + str(self.car_frequency_warning) + " Hz")

        return self.information, self.outputimage, self.battery

        
    # Add spaces to a string to match required lenght
    def fixedWidth(self,input,lenght):
    
        string = str(input)
        for i in range(lenght-len(string)):
            string += " "
        return string


    # From makemovie DK part
    def draw_user_input_fc(self, img):
        '''
        Draw the user input as a green line on the image
        '''

        import cv2

        user_angle = self.angle
        user_throttle = self.throttle

        height, width, _ = img.shape

        length = height
        a1 = user_angle * 45.0
        l1 = user_throttle * length

        mid = width // 2 - 1

        p1 = tuple((mid - 2, height - 1))
        p11 = tuple((int(p1[0] + l1 * math.cos((a1 + 270.0) * self.deg_to_rad)),
                     int(p1[1] + l1 * math.sin((a1 + 270.0) * self.deg_to_rad))))

        # user is green, pilot is blue
        return cv2.line(img, p1, p11, (0, 255, 0), 2)
