#F&C Sound part
import os
import time
from pygame import mixer

class FC_Sound:
    def __init__(self, cfg):
        self._on = True
        self.cfg = cfg
        self.lastFCMessageIndex = 0
        currentPath = __file__

        # Such a dirty way to change path : :)
        self.soundsBasePath = currentPath.replace('parts/fc_sound.py', 'media/sounds/').replace('parts\\fc_sound.py', 'media\\sounds\\')
        self.musicsBasePath = currentPath.replace('parts/fc_sound.py', 'media/musics/').replace('parts\\fc_sound.py', 'media\\musics\\')

        self.soundToPlay = ""
        mixer.init()

        self.play_sound("init.wav")
        print("F&C : Sound part activated.")


    def update(self):
        while self._on:
            if not (self.soundToPlay == ""):
                self.play_sound(self.soundToPlay)
                self.soundToPlay = ""
            else:
                time.sleep(0.1)

    def run_threaded(self, fc_messages):
        newFCMessage = False

        #Only keep last message
        if type(fc_messages) is list and (not len(fc_messages) == self.lastFCMessageIndex):
            self.lastFCMessageIndex = len(fc_messages)
            newFCMessage = True
        
        #A new message just arrived !
        if (newFCMessage):
            message = fc_messages[-1]

            # Choose sound file depending on message type :
            if ("Waiting for green light" in message):
                self.soundToPlay = "warmup_short.wav"
            
            elif ("STARTING RACE !" in message):
                self.soundToPlay = "startup_short.wav"
  
            elif ("NEW LAP RECORD !" in message):
                self.soundToPlay = "newlaprecord_short.wav"

            elif ("New lap" in message):
                self.soundToPlay = "newlap_short.wav"

            elif ("END OF RACE !" in message):
                self.soundToPlay = "end.wav"

                            
    def shutdown(self):
        self._on = False
        print('F&C : Stopping sound part.')
        time.sleep(.2)
   

    # F&C : Play a sound file
    def play_sound(self, soundFilePath):
        # Adding base path to media path
        soundFilePath = self.soundsBasePath + soundFilePath

        print("F&C : Playing sound '" + soundFilePath + "' ...")

        sound = mixer.Sound(soundFilePath)
        sound.set_volume(1.0)
        sound.play()
        #while mixer.get_busy() == True:
        #    continue

        # Insert sound logic here
        # https://pythonbasics.org/python-play-sound/
