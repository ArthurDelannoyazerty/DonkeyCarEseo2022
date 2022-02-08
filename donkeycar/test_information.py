import time

class TestInformation:
    def __init__(self):
        print('--------------INFO : Starting part')
        self.car_frequency = 0

    def run(self):
        print('--------------INFO : Running part')
        self.car_frequency  = 1/(time.time()-self.last_calc_time)
        self.last_calc_time = time.time()
        print("Frequency" + str(self.car_frequency) + " Hz")