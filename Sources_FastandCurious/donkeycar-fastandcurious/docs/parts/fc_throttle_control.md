# F&C custom throttle optimizations

This part is used for :

* growing the throttle on every lap to get the best lap time
* growing the throttle when battery go low to keep the same performance
* growing the throttle when the car is in a straight line to optimize AI output.

## Software Setup

Add this part in the compelete.py :

```
        from donkeycar.parts.fc_throttle_control import FC_Throttle_Control
        V.add(FC_Throttle_Control(cfg), inputs=['user/mode', 'pilot/angle', 'pilot/throttle', 'fc_current_lap', 'fc_messages'], outputs=['pilot/throttle', 'fc_multiplier', 'fc_currentthrottle_info', 'fc_messages'])
```

Add some lines in your myconfig.py :

* Activate lap increment on every lap :
```
THROTTLE_CONTROL_LAP_INCREMENT = 0.05
```
with this default configuration you can add 5% on the throttle command on each new lap (first lap 100%, 2nd 105%, 3tr 110%...)

* Activate battery optimization :
```
THROTTLE_CONTROL_POWEROPTIMIZATION = True      # Enabling Throttle optimization on battery discharge
THROTTLE_CONTROL_POWEROPTIMIZATION_HIGH_THRESHOLD = 70 # No throttle correction over this power remaining threshold
THROTTLE_CONTROL_POWEROPTIMIZATION_TOOLOW_THRESHOLD = 20 # Disable throttle correction when power remaining is under this threshold
THROTTLE_CONTROL_POWEROPTIMIZATION_MULTMAX = 0.2    # Max increm in lowest power (near THROTTLE_CONTROL_POWEROPTIMIZATION_TOOLOW_THRESHOLD)
```
With this default configuration you can add up to 20% on the throttle command when battery are very low

* Activate straight line optimization :
```
THROTTLE_CONTROL_AUTO_MAX_AMP = 0.25            # Activate the straight multiplier (0 to disable)
THROTTLE_CONTROL_AUTO_MAX_BREAK = 1.0           # Maximal negative Increm for break sequence 
THROTTLE_CONTROL_AUTO_INCREMENT = 0.005         # Start Power Increment
THROTTLE_CONTROL_AUTO_MAXIMAL_FIFO = 40         # Historical FIFO
THROTTLE_CONTROL_AUTO_MINIMAL_FIFO = 5          # Define number off break sequence (1 to Maximal FIFO)
THROTTLE_CONTROL_AUTO_LOWANGLE_THRESHOLD = 0.2  # under this absolute angle value the multiplier increase
THROTTLE_CONTROL_AUTO_HIGHANGLE_THRESHOLD = 0.4 # over this absolute angle value the break sequence is engaged
```

The FIFO mechanics is important to understand the speed increase.

A straight line is defined by a steering angle under the LOWANGLE_THRESHOLD percent and a high curve is a AI steering angle over the HIGHANGLE_THRESHOLD.

During a straight line, the part increase the AI throttle command up to the AUTO_MAX_AMP value (by default +25%). The increase speed depends of the AUTO_INCREMENT and the MAXIMAL_FIFO.

The FIFO corresponds to the number of car cycles that must be passed before increasing the coefficient. A short number increase more quickly but less linear and could increase suddenly acceleration.

The MINIMAL_FIFO is used when the car enter in a high curve. The part revert the acceleration ratio to a minus value to use break during the time defined by the MAXIMAL_FIFO to the MINIMAL_FIFO.

