# F&C custom sensor part to do avoidance

This part is used to exploit ultrasonic sensor and doing avoidance.

This part is designed to get values from a Rasp pico by usb port.

## Software Setup

Two functions need to add in the complete.py.
* The first is the collecting asynchronous tread (getting values from pico)
```
        from donkeycar.parts.fc_collision_detection import FC_Collision_Detection
        V.add(FC_Collision_Detection(cfg), 
                inputs=[],
                outputs=['ultra/dist_g', 'ultra/dist_c', 'ultra/dist_d',
                            'ultra/appr_g', 'ultra/appr_c', 'ultra/appr_d', 'fc_ultrasonic_info'],
                threaded=True)
```


* The second is the throttle and steering control :
```
        from donkeycar.parts.fc_collision_detection import FC_AvoidanceStrategy
        V.add(FC_AvoidanceStrategy(cfg), 
                inputs=['user/mode', 'pilot/angle', 'pilot/throttle', 'ultra/dist_g', 'ultra/dist_c', 'ultra/dist_d', 'ultra/appr_g', 'ultra/appr_c', 'ultra/appr_d', 'fc_messages'],
                outputs=['pilot/angle', 'pilot/throttle', 'fc_messages'])
```
This function use all informations to decide if we need to slow down, turn or stop the car.

In the myconfig.py you have two parts :
* Configuring pico asynchronous collect
```
FC_ULTRASENSOR_REFRESH_FREQUENCY = 0.025        # 0.025 every 25msec
FC_ULTRASENSOR_DISTANCE_HISTORY = 10            # Number of records use for arithmetic mean 
```

* Enable and configure avoidance mechanic
```
ULTRASONIC_SENSOR_AVOIDANCE = False             # Enable interactivity with ultrasonic senor results
FC_AVOIDANCE_ANGLEHELPER = True                 # Can force steering for avoidance
FC_AVOIDANCE_SPEEDLIMIT = 0.4                   # Throttle limit during avoidance step
FC_AVOIDANCE_EMERGENCYDISTANCE = [15,25,50,80]  # 4 param in cm ; 1st = under this the car stopped ; under the 3rd avoidance start ; under the 4th only notify detection
```