#F&C Throttle Control part

# If necessay, import required parts here :
import queue
import os   # For i2detect

class AccelerationInfo:
  def __init__(self, angle, action = 'NONE', multiplicator = 0, lastPowerMedium = 0, type = 'Unknown', throttle = 0):
    self.currentAngle = angle
    self.multiplicator = multiplicator
    self.action = action
    self.angle = angle
    self.type = type
    self.lastPowerMedium = lastPowerMedium
    self.throttle = throttle


class FC_Throttle_Control:
    def __init__(self, cfg):
        self.cfg = cfg
        self.defaultMultiplier = cfg.THROTTLE_CONTROL_DEFAULT_MULT
        self.lapIncrement = cfg.THROTTLE_CONTROL_LAP_INCREMENT
        self.lastLapValue = 1
        
        #
        self.MaxPowerAmp = cfg.THROTTLE_CONTROL_AUTO_MAX_AMP
        self.MaxBreakAmp = cfg.THROTTLE_CONTROL_AUTO_MAX_BREAK
        self.coefAccIterration = cfg.THROTTLE_CONTROL_AUTO_INCREMENT
        self.MinimumHistorical = cfg.THROTTLE_CONTROL_AUTO_MINIMAL_FIFO
        self.LowAngleThreshold = cfg.THROTTLE_CONTROL_AUTO_LOWANGLE_THRESHOLD
        self.HighAngleThreshold = cfg.THROTTLE_CONTROL_AUTO_HIGHANGLE_THRESHOLD
        self.lastMessage = AccelerationInfo(0)
        self.historicalPower = queue.Queue(cfg.THROTTLE_CONTROL_AUTO_MAXIMAL_FIFO)

        #
        self.powerOptimization = cfg.THROTTLE_CONTROL_POWEROPTIMIZATION
        self.powerHighThreshold = cfg.THROTTLE_CONTROL_POWEROPTIMIZATION_HIGH_THRESHOLD
        self.powerOptimMax = cfg.THROTTLE_CONTROL_POWEROPTIMIZATION_MULTMAX
        self.powerTooLowThreshold = cfg.THROTTLE_CONTROL_POWEROPTIMIZATION_TOOLOW_THRESHOLD
        
        if self.powerOptimization:
            from donkeycar.management.ina219 import INA219
            from donkeycar.management.ads1115 import ADS1115

            adress = os.popen("i2cdetect -y -r 1 0x48 0x48 | egrep '48' | awk '{print $2}'").read()
            if(adress=='48\n'):
                self.ads = ADS1115()
            else:
                self.ads = None
                
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
        

        print("F&C : Throttle Control part activated.")
        
        if not (cfg.AI_THROTTLE_MULT == 1.0):
            print("F&C : WARNING : AI_THROTTLE_MULT is enabled ! (should be kept at 1.0)")    

    def run(self, mode, angle, throttle=0, lap=0, fc_messages=["","",""]):
        multiplier = 1.0
                
        # Only work during local pilot mode
        if (mode == 'local'):
            multiplier = self.defaultMultiplier

            # Increment value at each lap
            if (lap > self.lastLapValue):
                self.lastLapValue = lap
                self.defaultMultiplier += self.lapIncrement
                multiplier = self.defaultMultiplier
            
            # Increment value when Batterie Power is low
            if self.powerOptimization:
                if(self.ina != None):
                    bus_voltage = self.ina.getBusVoltage_V()        # voltage on V- (load side)
                    p = (bus_voltage - 6)/2.4*100
                elif(self.ina219 != None):
                    bus_voltage = self.ina219.getBusVoltage_V()        # voltage on V- (load side)
                    dichargePercent = (bus_voltage - 9)/3.6*100
                elif(self.ads != None):
                    value=self.ads.readVoltage(4)/1000.0
                    dichargePercent = value/12.6*100
                
                if(dichargePercent > 100):dichargePercent = 100
                if(dichargePercent < 0):dichargePercent = 0
                
                if dichargePercent < self.powerHighThreshold and dichargePercent > self.powerTooLowThreshold:
                    powerMult = ((dichargePercent - self.powerHighThreshold) / (self.powerHighThreshold - self.powerTooLowThreshold))*self.powerOptimMax
                    multiplier += powerMult
                    if type(fc_messages) is list:
                        fc_messages.append("Power Mult " + str(powerMult) + " for batterie in " + str(dichargePercent) + "% (" + str(multiplier) + ")")
                
            # Increment value when angle is low
            if self.MaxPowerAmp > 0.000:
                    # Init de la sortie d'informations
                message = AccelerationInfo(0, angle)
                lastPowerMedium = 0
                #
                # Determine la valeur d'amplification importance plus élevée sur la dernière valeur
                # pour optimiser l'acceleration ou le freinage
                lastAcceleration = AccelerationInfo(0, 0)
                currentHistoricalNb = self.historicalPower.qsize() 
                backHistoricalPower = queue.Queue(currentHistoricalNb)
                throttleMedium = throttle
                
                while not self.historicalPower.empty():
                  lastAcceleration = self.historicalPower.get()
                  if lastAcceleration.action != 'DOWN':
                    lastPowerMedium += lastAcceleration.multiplicator
                  throttleMedium += lastAcceleration.throttle
                  backHistoricalPower.put(lastAcceleration)
                  
                if currentHistoricalNb > 0:
                    lastPowerMedium = lastPowerMedium / currentHistoricalNb
                    throttleMedium = throttleMedium / currentHistoricalNb
                
                self.historicalPower = backHistoricalPower
                
                lastPowerMedium = round(lastPowerMedium, 5)
                message.lastPowerMedium = lastPowerMedium
                # Acceleration progressive jusqu'a atteinte de la limite
                if abs(angle) < self.LowAngleThreshold:
                    message.type = "Low angle"
                    
                    if self.historicalPower.full():
                        deprecatedValue = self.historicalPower.get()

                    message.action = 'UP'
                    if lastPowerMedium < 0:
                        message.action = 'NONE'
                        message.multiplicator = 0
                    
                    elif throttleMedium > throttle:
                        # Deleration de l'IA -> Reduction du multiplicateur
                        message.action = 'DOWN'    
                        message.type = "Throttle decreasing"
                        message.multiplicator = lastPowerMedium  / 2
                    
                    elif lastPowerMedium == 0.000:
                        # On lance l'acceleration
                        message.multiplicator = self.coefAccIterration
                        
                    elif lastPowerMedium >= self.MaxPowerAmp:
                        # L'accelération max est atteinte
                        message.multiplicator = lastPowerMedium

                    elif lastPowerMedium < lastAcceleration.multiplicator:
                        # Il faut attendre que tous les points soit a la même valeur pour augmenter la vitesse
                        message.multiplicator = lastAcceleration.multiplicator

                    elif lastPowerMedium * 2 > self.MaxPowerAmp:
                        # Atteinte de l'acceleration max
                        message.multiplicator = self.MaxPowerAmp

                    else:
                        # on augmente l'acceleration
                        message.multiplicator = round(lastPowerMedium * 2, 2)
                
                # Freinage ou arrêt du multiplicateur
                elif abs(angle) > self.HighAngleThreshold:
                    message.type = "High angle"
                    if self.historicalPower.qsize() > 0:
                        deprecatedValue = self.historicalPower.get()

                    if self.historicalPower.qsize() > self.MinimumHistorical:
                        deprecatedValue = self.historicalPower.get()
                    
                    message.action = 'DOWN'    
                    if lastPowerMedium > 0.000:
                        message.multiplicator = -lastPowerMedium
                        
                    else:
                        message.multiplicator = 0
                
                # Maintien du multiplicateur de vitesse
                else:
                    message.type = "Medium angle"
                    if self.historicalPower.qsize() > 0:
                        deprecatedValue = self.historicalPower.get()
                    
                    if lastPowerMedium < 0:
                        message.action = 'NONE' 
                        message.multiplicator = 0
                        
                    else:
                        message.action = 'REGUL'
                        message.multiplicator = lastPowerMedium
                
                self.historicalPower.put(message)
                self.lastMessage = message
                multiplier += message.multiplicator
                
                if message.multiplicator != 0.000 and (lastAcceleration.multiplicator != message.multiplicator or lastAcceleration.action != message.action):
                    if type(fc_messages) is list:
                        from datetime import datetime
                        now = datetime.now()
                        myInfo = now.strftime("%X.%f") + " - Angle Mult : " + message.type + " - " + message.action + " - " + str(message.multiplicator) + " (" + str(multiplier) + ")"
#                        print(myInfo+"\n")
#                        fc_messages.append(myInfo)


            # Applying throttle multiplier
            throttle = throttle * multiplier

        return throttle, multiplier, self.lastMessage, fc_messages

