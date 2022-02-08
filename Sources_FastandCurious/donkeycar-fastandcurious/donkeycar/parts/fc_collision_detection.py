#F&C Collision detection part

# If necessay, import required parts here :
from gpiozero import InputDevice, OutputDevice
import time, os
import json
from multiprocessing import Process, Queue
import numpy as np

FC_AVOIDANCE_FLG_EMERGENCY = 10
FC_AVOIDANCE_FLG_AVOIDANCE_REQUIRED = 5 
FC_AVOIDANCE_FLG_COMEBACK_SLOWLY = -5
FC_AVOIDANCE_FLG_AVOIDANCE_COULDBENEED = 1
FC_AVOIDANCE_FLG_NOTHING = 0


class FC_Collision_Detection:

    def __init__(self, cfg):
        self.cfg = cfg
        self.sensorList = []
        self.lastGetDistance = {}
        self.currentGetDistance = {}
        self.prevDistanceList = {}
        self.scanFrequency = cfg.FC_ULTRASENSOR_REFRESH_FREQUENCY # 0.025
        self.prevDistanceLen = cfg.FC_ULTRASENSOR_DISTANCE_HISTORY # 10
        self.port = False
        if os.path.exists('/dev/ttyACM0') == True:
            self.port = '/dev/ttyACM0'
        elif os.path.exists('/dev/ttyACM1') == True:
            self.port = '/dev/ttyACM1'
        if type(self.port) == str:
            import serial
            print("Connect to Serial :", self.port)
            self.ser = serial.Serial(self.port, 115200)
            print(self.ser)
            self.on = True
        else:
            print("unable to find serial port")
            self.on = False
        
        print("F&C : Collision Detection part activated.")

    def update(self):
        print("F&C : Starting Collision Detection.")
        while self.on:
            command = str("all") + "\n"
            self.ser.write(bytes(command.encode('ascii')))
            pico_data = self.ser.readline()
            pico_data = pico_data.decode("utf-8","ignore")
            self.sensorList =  json.loads(pico_data[:-2])
            for sensor in self.sensorList:
                # Correcting real distance according sensor position on the car
                if sensor["Angle"] == 0 and sensor['distance'] < 150:
                    sensor['distance'] -= 2
                elif sensor["Angle"] > 0 and sensor['distance'] < 150:
                    sensor['distance'] -= 7
                # init distance history list for this sensor
                if sensor["Angle"] not in self.prevDistanceList:
                   self.prevDistanceList[sensor["Angle"]] = []
                self.prevDistanceList[sensor["Angle"]].append(sensor['distance'])
                # Limit distance history to defined number
                while len(self.prevDistanceList[sensor["Angle"]]) > self.prevDistanceLen:
                    self.prevDistanceList[sensor["Angle"]].pop(0)
                # getout abnormal value
                valmedian = np.median(np.array(self.prevDistanceList[sensor["Angle"]]))
                valq1 = np.percentile(np.array(self.prevDistanceList[sensor["Angle"]]), 25)
                valq3 = np.percentile(np.array(self.prevDistanceList[sensor["Angle"]]), 75)
                valecart = valq3 - valq1
                if sensor['distance'] < (valq1 - (1.5*valecart)) :
                    sensor['distance'] = int(valmedian)
                elif sensor['distance'] > (valq3 + (1.5*valecart)):
                    sensor['distance'] = int(valmedian)
                # Record the retained value for this sensor
                self.currentGetDistance[sensor["Angle"]] = sensor['distance']
                
            time.sleep(self.scanFrequency)
        print("F&C : Collision Detection stopped.")
                
    def run_threaded(self):
        currentState = []
        try:
            for sensor in self.sensorList:
                if sensor["Angle"] in self.lastGetDistance:
                    distance = self.currentGetDistance[sensor["Angle"]] 
                    approach = self.lastGetDistance[sensor["Angle"]] - distance
                else:
                    approach = 0
                    distance = 300
                currentState.append({"Angle": sensor['Angle'],"approach": approach, "distance": distance})
                self.lastGetDistance[sensor["Angle"]] = sensor['distance']
        except:
            print('FC_Collision_Detection: unable to get values.')
            
        if len(currentState) < 3:
            return 300, 300, 300, 0, 0, 0, currentState
        else:
            return currentState[0]['distance'], currentState[1]['distance'], currentState[2]['distance'], currentState[0]['approach'], currentState[1]['approach'], currentState[2]['approach'], currentState
        
    def shutdown(self):
        print("F&C : Stopping Collision Detection part.")
        self.on = False

class FC_AvoidanceStrategy:
    def __init__(self, cfg):
        self.cfg = cfg
        self.previousAction = FC_AVOIDANCE_FLG_NOTHING
        self.avoidanceSpeedLimit = cfg.FC_AVOIDANCE_SPEEDLIMIT # 0.4
        self.emergencyDistance = cfg.FC_AVOIDANCE_EMERGENCYDISTANCE # [15,25,50,80] 
        self.angleHelper = cfg.FC_AVOIDANCE_ANGLEHELPER # True
        print("F&C : Avoidance Strategy part activated.")

    def run(self, mode, angle, throttle=0, dist_g=300, dist_c=300, dist_d=300, appr_g=0, appr_c=0, appr_d=0, fc_messages=["","",""]):
        fc_coldetect_distance = [dist_g, dist_c, dist_d]
        fc_coldetect_approach = [appr_g, appr_c, appr_d]
        sensorFlag = []
        if mode == 'local':
            sensorSeverity = FC_AVOIDANCE_FLG_NOTHING
            for i in range(len(fc_coldetect_distance)):
                distance = fc_coldetect_distance[i]
                approach = fc_coldetect_approach[i]
                flagValue = FC_AVOIDANCE_FLG_NOTHING
                if distance < self.emergencyDistance[0] :
                    # object is under 10 centimeters 
                    flagValue = FC_AVOIDANCE_FLG_EMERGENCY
                elif distance < self.emergencyDistance[1] and approach < 0:
                    # object is under 20 centimeters but go away
                    flagValue = FC_AVOIDANCE_FLG_COMEBACK_SLOWLY
                elif distance < self.emergencyDistance[2] and approach > 0:
                    # object is under 40 centimeters and in approach
                    flagValue = FC_AVOIDANCE_FLG_AVOIDANCE_REQUIRED
                elif distance < self.emergencyDistance[3] and approach > 0:
                    # object is under 80 centimeters and in approach
                    flagValue = FC_AVOIDANCE_FLG_AVOIDANCE_COULDBENEED
                sensorSeverity += flagValue
                sensorFlag.append(flagValue)
            
            if sensorSeverity >= 2 * FC_AVOIDANCE_FLG_EMERGENCY and fc_coldetect_distance[1] < self.emergencyDistance[0] :
                if throttle > 0 and self.previousAction != FC_AVOIDANCE_FLG_EMERGENCY:
                    throttle = -1
                else:
                    throttle = 0
                if self.previousAction != FC_AVOIDANCE_FLG_EMERGENCY:
                    fc_messages.append("EMERGENCY STOP ! object is less than 10cm on every sensors.")
                    self.previousAction = FC_AVOIDANCE_FLG_EMERGENCY
                    
            elif sensorSeverity >= FC_AVOIDANCE_FLG_EMERGENCY:
                if throttle > self.avoidanceSpeedLimit:
                    throttle = self.avoidanceSpeedLimit
                if (fc_coldetect_distance[1] < self.emergencyDistance[0] or fc_coldetect_distance[1] <  self.emergencyDistance[2]) and self.angleHelper:
                    if fc_coldetect_distance[0] > fc_coldetect_distance[2] and angle < 0:
                        angle = -1
                    elif fc_coldetect_distance[0] < fc_coldetect_distance[2] and angle > 0:
                        angle = 1
                
                if self.previousAction !=  FC_AVOIDANCE_FLG_AVOIDANCE_REQUIRED:
                    fc_messages.append("AVOIDANCE REQUIRED ! Speed limited to : " + str(self.avoidanceSpeedLimit))
                    self.previousAction = FC_AVOIDANCE_FLG_AVOIDANCE_REQUIRED
            
            elif self.previousAction != FC_AVOIDANCE_FLG_NOTHING:
                fc_messages.append("AVOIDANCE return normal state.")
                self.previousAction = FC_AVOIDANCE_FLG_NOTHING
            
            
        return angle, throttle, fc_messages

    def shutdown(self):
        print("F&C : Stopping Avoidance Collision part.")

