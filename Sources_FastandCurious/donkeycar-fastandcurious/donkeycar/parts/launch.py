import time

class AiLaunch():
    '''
    This part will apply a large thrust on initial activation. This is to help
    in racing to start fast and then the ai will take over quickly when it's
    up to speed.
    '''

    def __init__(self, launch_duration=1.0, launch_throttle=1.0, keep_enabled=False):
        self.active = False
        self.enabled = False
        self.timer_start = None
        self.timer_duration = launch_duration
        self.launch_throttle = launch_throttle
        self.prev_mode = None
        self.trigger_on_switch = keep_enabled
        self.displayed = False # F&C : Minor change to avoid message

    def enable_ai_launch(self):
        self.enabled = True
        print('AiLauncher is enabled.')

    def run(self, mode, ai_throttle, fc_messages): # F&C : Minor change to add message
        new_throttle = ai_throttle

        if mode != self.prev_mode:
            self.prev_mode = mode
            if mode == "local" and self.trigger_on_switch:
                self.enabled = True

        if mode == "local" and self.enabled:
            if not self.active:
                self.active = True
                self.timer_start = time.time()
            else:
                duration = time.time() - self.timer_start
                if duration > self.timer_duration:
                    self.active = False
                    self.enabled = False
        else:
            self.active = False

        if self.active:
            if not self.displayed:
                self.displayed = True # F&C : Minor change to avoid spam
                fc_messages.append('Startup boost enabled for ' + str(self.timer_duration) + " sec !")
            
            new_throttle = self.launch_throttle

        return new_throttle, fc_messages # F&C : Minor change to add message

