# F&C custom LED card

This part is used to show visual information about the car during the race. 

The leds module is connected to raspberry GPIO with 2 green and 2 red led.

In this version we only use 2 led :
* the green led to show throttle acceleration ratio over the IA output.
* a red led to show a reduced throttle than the IA output.

This part is asynchronous with a thread.

We use the fc_currentthrottle_info parameters to update the status.

## Software Setup

To add this part in you complete.py : 
```
        from donkeycar.parts.fc_led import FC_Led
        fcled = FC_Led(cfg)
        V.add(fcled, inputs=['fc_currentthrottle_info'], threaded=True)
```

In the myconfig.py add GPIO Ports information like :
```
FCLED_GPIO_RED1 = 20
FCLED_GPIO_RED2 = 13
FCLED_GPIO_GREEN1 = 16
FCLED_GPIO_GREEN2 = 21
```