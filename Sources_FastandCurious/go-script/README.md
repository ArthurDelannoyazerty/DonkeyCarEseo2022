Fast&Curious
Script de gestion Donkey Car pour PI et PC (miniconda).

![go-script](https://gitn.sigma.fr/sigma/ia-racing/fastandcurious/go-script/-/raw/master/Capture.png)

# Autostart script on PI

## Install Autostart Service on PI

In pi user :
```
sudo cp ./projects/go-script/pi/fc_autostart.service /etc/systemd/system
sudo -S systemctl enable fc_autostart
sudo -S systemctl start fc_autostart
```

To check the service and last logs :
```
sudo -S systemctl status fc_autostart
```

To Stop the service :
```
sudo -S systemctl stop fc_autostart
```

## Usage

The picture below shows the car control board.

![child board](/images/lb_board.png)

To interact with the autostart script you can use 2 button and 2 leds.

When the autoload deamon start, the green light flashes slowly. At this step the daemon wait you to push the right button to start the donkeycar programme.

During load Green and Red lights flashes slowly. When the car is ready (you can connect to the webconsole), only the green light flashes quickly.

The car waiting you to do an action, you can use joystick or webconsole or you can press the right button to turn the car in the race mode.

In the race mode, when the car wait for the starting light, green and red lights flashes quickly.

When the starting light is detected by fc_race part, the red light turn off and the green light staying on.

At the end of the race, when the number of laps is reached, the red light is turned on and green ligth flashing quickly.

At every time you can stop the donkeycar program by pressing the left button. When you do that the program stop python donkeycar program and return to the first status (green light flashing slowly).

![child board](/images/autostart_steps.png)


