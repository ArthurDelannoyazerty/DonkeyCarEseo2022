# Auto-Start script
#
import logging
import threading
from time import sleep,time
from gpiozero import LED, Button
import psutil
import os
import re
import subprocess
import requests
import sys
import signal

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

# Recuperer le nom du fichier du configuration du script

script = os.path.realpath(__file__)
print("SCript path:", script)
import json
with open(script.replace(".py", ".json")) as json_config_file:
    config = json.load(json_config_file)

# Recuperer le nom du fichier de PID dans la configuration
if 'goPidFile' not in config:
    config['goPidFile'] = "/tmp/go.pid"

# Recuperer le chemin du programme python
if "pythonPath" not in config:
    config['pythonPath'] = "/home/pi/env/bin/python"

# Recuperer le chemin de la voiture
if "carPath" not in config:
    config['carPath'] = "/home/pi/fc_cars/testcar"

if not os.path.exists(config["carPath"]):
    print("Unable to find car path : " + config["carPath"])
    exit(1)
carManageFile = config["carPath"]+"/manage.py"
if not os.path.exists(carManageFile):
    print("Unable to find "+carManageFile)
    exit(1)
# Recuperer le modele d'IA a executer
if 'carModel' not in config:
    print("Unable to find carModel in configfile!")
    exit(1)

if not os.path.exists(config["carModel"]):
    print("Unable to find car Modele : "+config["carModel"])
    exit(1)
# Recupere l'URL d'api du manage
if 'driveURL' not in config:
    config['driveURL'] = 'http://localhost:8887/drive'

# Recupere la liste des services a desactive
listDisableService = ['picard_display', 'bluetooth']
if 'disabledServicesDuringRace' in config:
    listDisableService = config["disabledServicesDuringRace"]

# Get Red Led IO port
ledRIOPort = 13
if 'ledRIOPort' in config:
    ledRIOPort = config["ledRIOPort"]
ledGIOPort = 21
if 'ledGIOPort' in config:
    ledGIOPort = config["ledGIOPort"]
cmdRightButtonIOPort = 26
if 'rightButtonIOPort' in config:
    cmdRightButtonIOPort = config["rightButtonIOPort"]
cmdLeftButtonIOPort = 19
if 'leftButtonIOPort' in config:
    cmdLeftButtonIOPort = config["leftButtonIOPort"]


statusList = ["None","Need Press Start Button","Drive Programme Loading","Drive Loaded","Waiting for green light","Running","End of Race detected"]
threadAutopilot = None


class autopilotThread(threading.Thread):
    def __init__(self, currentStep):
        threading.Thread.__init__(self)
        self.startingCmd = [config['pythonPath'], "-u", carManageFile, "drive"]
        self.startingCmd.append("--model="+ config["carModel"])
        if re.search('.tflite$', config["carModel"]):
            self.startingCmd.append("--type=tflite_linear")	
        
        self.driveProc = None
        self._running = True
        
        # Add stopping system services that we don't need during the race
        for serviceName in listDisableService:
            logging.info("Stop system service : ",serviceName)
            try:
                command = subprocess.run(['sudo', 'systemctl', 'stop', serviceName], capture_output=True)
                sys.stdout.buffer.write(command.stdout)
                sys.stderr.buffer.write(command.stderr)
            except e:
                logging.info("Unable to stop service :",serviceName)
                logging.info(e)
            
        logging.info("Autopilot Thread initialized.")
        return

    def run(self):
        logging.info("Starting car with : ")
        global currentStep
        logging.info(self.startingCmd)
        self.driveProc = subprocess.Popen(self.startingCmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) #, stderr=subprocess.PIPE)
        
        while self._running and self.driveProc.poll() is None:
            #if True == False:
            for stdout_bytes in iter(self.driveProc.stdout.readline, b''):
                if sys.getsizeof(stdout_bytes) < 28:
                    continue
                stdout_line = stdout_bytes.strip().decode('UTF-8')
                logging.info(stdout_line)
                
                
                #logging.info("Autopilot: " + stdout_line)
                # detecter la voiture charger et changer le mode de clignottement de la led pour le haut bas & changer le currentstep
                if currentStep == 2 and re.search('^Starting vehicle at', stdout_line) :
                    logging.info("Autopilot => car starded detected")
                    logging.info("Up/Down for cam needed")
                    currentStep = 3
                
                # detecter l'etat Ready de la voiture / Attente du feu vert
                # "^Waiting for green light"
                elif currentStep > 2 and re.search('^F&C : waiting for green light', stdout_line):
                    logging.info("Autopilot => car waiting green light detected")
                    currentStep = 4
                    
                # detecter la detection du signalfeu vert
                # "^Green light detected"
                elif currentStep > 2 and re.search('^F&C : Green light detected', stdout_line):
                    logging.info("Autopilot => car running detected")
                    currentStep = 5
                
                # detecter la fin de course
                # "^END OF RACE !"
                elif currentStep > 2 and re.search('^F&C : END OF RACE detected', stdout_line):
                    logging.info("Autopilot => End of race detected")
                    currentStep = 6
                
            logging.info("Flush")
            sleep(1)
            
        try:
            self.driveProc.stdout.close()
            self._running = False
            if self.driveProc.poll() is None:
                # Stop the car process
                self.driveProc.terminate()
            waitSec = 10
            while self.driveProc.poll() is None and waitSec > 0:
                sleep(1)
                waitSec -= 1
            if self.driveProc.poll() is None:
                # Hard kill
                self.driveProc.kill()
        except e:
            logging.info("Unable to kill proc")
            logging.info(e)
        currentStep = 1
        logging.info("Autopilot Stopped")
        return

    def stop(self):
        logging.info("Stopping autopilot...")
        try:
            myobj = {"angle": 0, "throttle": 0, "drive_mode": "user", "recording": "false", "fcsetting": ":"}
            x = requests.post(config["driveURL"], json = myobj)
            logging.info(x.text)
        except e:
            logging.info("Unable to send user mode")
            logging.info(e)
        self._running = False
        self.driveProc.terminate()
        self.driveProc.stdout.close()
        waitSec = 10
        while self.driveProc.poll() is None and waitSec > 0:
            sleep(1)
            waitSec -= 1
        if self.driveProc.poll() is None:
            # Hard kill
            self.driveProc.kill()
        
        # Start system services previously stopped during the race
        for serviceName in listDisableService:
            logging.info("Starting system service : ",serviceName)
            try:
                command = subprocess.run(['sudo', 'systemctl', 'start', serviceName], capture_output=True)
                sys.stdout.buffer.write(command.stdout)
                sys.stderr.buffer.write(command.stderr)
            except e:
                logging.info("Unable to start service :",serviceName)
                logging.info(e)
        
        return

def whenPressLeft():
    start_time = time()
    global leftButton
    logging.info("Button Left pressed.")
    global currentStep
    global threadAutopilot
    hold_time = 2 # in second
    diff = 0
    
    while leftButton.is_active and (diff <hold_time) :
        now_time=time()
        diff=-start_time+now_time
    
    if currentStep > 1:
        # Mettre fin a l'autopilote
        threadAutopilot.stop()
        logging.info("Waiting end of Autopilot Thread...")
        threadAutopilot.join()
        currentStep = 1
    logging.info(diff)
    if diff >= hold_time :
        logging.info("User want to stop the pi")
        command = subprocess.run(['sudo', 'init', '0'], capture_output=True)
        sys.stdout.buffer.write(command.stdout)
        sys.stderr.buffer.write(command.stderr)
 
    logging.info("Exit button Left action.")
    return

def whenPressRight():
    logging.info("Button Right pressed.")
    global currentStep
    global threadAutopilot
    if currentStep == 1:
        # Starting Autopilot Thread
        logging.info("Starting Autopilot Thread...")
        threadAutopilot = autopilotThread(currentStep)
        threadAutopilot.start()
        currentStep = 2

    elif currentStep == 3:
        # Le hautbas est effectue => Declanchement du mode "attente du feu vert"
        myobj = {"angle": 0, "throttle": 0, "drive_mode": "waiting", "recording": "false", "fcsetting": ":"}
        x = requests.post(config["driveURL"], json = myobj)
        logging.info(x.text)
        
    logging.info("Exit button Right action.")
    return

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


def checkIfGOProcessRunning(cfg):
    try:
        with open(cfg['goPidFile'], 'r') as pidFile:
            pidline = pidFile.readline().splitlines()[0]
            if RepresentsInt(pidline):
              print(pidline)
              if psutil.pid_exists(int(pidline)):
                return True
            return False
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False

class ledFlashThread(threading.Thread):
    def __init__(self, currentStep, frequency=0.25):
        threading.Thread.__init__(self)
        self.frequency = frequency
        self._running = True
        logging.info("LED Thread initialized.")
        return
    
    def run(self):
        logging.info("Starting switching leds.")
        global currentStep
        ledR = LED(ledRIOPort)
        ledG = LED(ledGIOPort)
        while self._running:
            #print(currentStep)
            if currentStep == 1:
                # 1 => Green clignote 0.5
                if not ledG.value:
                    ledG.on()
                else:
                    ledG.off()
                if ledR.value:
                    ledR.off()
                sleep(1*self.frequency)
            elif currentStep == 2:
                # 2 => Green clignote 0.5 | Rouge clignote 0.5
                if not ledG.value:
                    ledG.on()
                    ledR.on()
                else:
                    ledG.off()
                    ledR.off()
                sleep(1*self.frequency)
            elif currentStep == 3:
                # 3 => Green clignote 0.25
                if not ledG.value:
                    ledG.on()
                else:
                    ledG.off()
                if ledR.value:
                    ledR.off()
                sleep(0.5*self.frequency)
            elif currentStep == 4:
                # 4 => Green clignote 0.25 | Rouge clignote 0.25
                if not ledG.value:
                    ledG.on()
                    ledR.on()
                else:
                    ledG.off()
                    ledR.off()
                sleep(0.5*self.frequency)
            elif currentStep == 5:
                # 5 => Green statique
                if not ledG.value:
                    ledG.on()
                if ledR.value:
                    ledR.off()
                sleep(1*self.frequency)
            elif currentStep == 6:
                # 6 => Green clignote 0.25 | Rouge statique
                if not ledG.value:
                    ledG.on()
                else:
                    ledG.off()
                if not ledR.value:
                    ledR.on()
                sleep(0.5*self.frequency)
                
        logging.info("Switching for leds stopped.")
        ledR.close()
        ledG.close()
        return

    def stop(self):
        logging.info("Stopping led Thread...")
        self._running = False
        return

def initButton():
    logging.info("Initialize Buttons")
    rightButton = Button(cmdRightButtonIOPort)
    rightButton.when_pressed = whenPressRight
    
    leftButton = Button(cmdLeftButtonIOPort)
    leftButton.when_pressed = whenPressLeft
    logging.info("Buttons initialized")
    return rightButton, leftButton

def stopButton(rightButton, leftButton):
    rightButton.close()
    leftButton.close()
    return
    


def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    threadAutopilot.stop()
    threadAutopilot.join()
    ledThread.stop()
    ledThread.join()
               
    logging.info("Autostart exit.")
    exit(0)
 
 
signal.signal(signal.SIGTERM, service_shutdown)
signal.signal(signal.SIGINT, service_shutdown)
logging.info("Initializing.")
try:

    #
    # Main
    currentStep = 0
    rightButton, leftButton = initButton()
    stopButton(rightButton, leftButton)

    logging.info("Starting autostart checking...")
    ledThread = ledFlashThread(currentStep, 0.5)
    ledThread.start()
    ledThread.stop()
    ledThread.join()
     
    while True:
        if checkIfGOProcessRunning(config): 
            if ledThread.is_alive():
                ledThread.stop()
                ledThread.join()
                stopButton(rightButton, leftButton)
                currentStep = 0
                logging.info("Stopped")
        elif not ledThread.is_alive():
            print("Not Alive")
            ledThread = ledFlashThread(currentStep, 0.5)
            ledThread.start()
            rightButton, leftButton = initButton()
            currentStep = 1
            logging.info("Started")
        sleep(3)
except ExitCommand:
    pass
finally:
        
    ledThread.stop()
    ledThread.join()
               
    logging.info("Autostart exit.")

    exit(0)
