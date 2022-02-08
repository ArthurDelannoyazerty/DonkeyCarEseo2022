#F&C Led part

# If necessay, import required parts here :
from gpiozero import PWMLED, LED, Button
from time import sleep

class SimulLed:
    def __init__(self, port):
        self.value = 0
        self.port = port
    
    def on(self):
        print("switch on port : " + str(self.port))
        self.value = 1
    
    def off(self):
        print("switch off port : " + str(self.port))
        self.value = 0

class FC_Led:
    def __init__(self, cfg):
        self.cfg = cfg
        if (not cfg.DONKEY_GYM) :
            self.led_red1 = LED(cfg.FCLED_GPIO_RED1)
            self.led_red2 = LED(cfg.FCLED_GPIO_RED2)
            self.led_green1 = LED(cfg.FCLED_GPIO_GREEN1)
            self.led_green2 = LED(cfg.FCLED_GPIO_GREEN2)
        else:
            self.led_red1 = SimulLed(cfg.FCLED_GPIO_RED1)
            self.led_red2 = SimulLed(cfg.FCLED_GPIO_RED2)
            self.led_green1 = SimulLed(cfg.FCLED_GPIO_GREEN1)
            self.led_green2 = SimulLed(cfg.FCLED_GPIO_GREEN2)

        from donkeycar.parts.fc_throttle_control import AccelerationInfo
        self.fc_currentthrottle_info = AccelerationInfo(0)
        
        self.on = True
        
        self.previous = 'NONE'

        print("F&C : Led part activated.")

    def update(self):
        while self.on:
            if self.fc_currentthrottle_info.multiplicator > 0 :
                sleep(0.25*(1-self.fc_currentthrottle_info.multiplicator))
                self.led_red1.off()
                if not self.led_green1.value:
                    self.led_green1.on()
                else:
                    self.led_green1.off()
            elif self.fc_currentthrottle_info.multiplicator < 0:
                self.led_green1.off()
                sleep(0.25*(1+self.fc_currentthrottle_info.multiplicator))
                if not self.led_red1.value:
                    self.led_red1.on()
                else:
                    self.led_red1.off()
            else:
                sleep(0.12)
                self.led_green1.off()
                self.led_red1.off()
            self.previous = self.fc_currentthrottle_info.action                
                
    def run_threaded(self, fc_currentthrottle_info):
        self.fc_currentthrottle_info = fc_currentthrottle_info

    def shutdown(self):
        self.on = False
        self.led_green1.off()
        self.led_red1.off()
