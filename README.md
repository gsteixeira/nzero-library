# Python library for NearZero(tm) Controllers - nzerolib

Python library to manage the [NearZero](https://github.com/jhaupt/NearZero1) Brushless Motor Controller for robotics.

Based in the examples of the [awesome work](https://www.youtube.com/watch?v=OZvjfbpXpro) made by [JHaupt](https://github.com/jhaupt). 

This does the same thing her examples do, but tries to be a reusable and distributable module.

With this you can:
- Sends data to a NearZero controller.
- Program Robot movements.
- Control a Robot with the keyboard.

Installation:
    
```shell
   pip install git+https://github.com/gsteixeira/nzero-library

```

Basic low level operation:
```python
from nzerolib import NZero
# instantiate NZ
Wheel = NZero("TheWheel", 0x40, 1)
velocity = 30
current = 20
# control the motor
Wheel.write('v', velocity, current)

```

Control the Robot:
```python
from nzerolib import Robot
import time
# The Robot will walk for two seconds, then stop
bot = Robot()
bot.go_forward()
time.sleep(2)
bot.stop_move()
```

Run without a real NearZero hardware (Debug Mode):
```python
# this makes data sent to the i2c interface be printed on screen
bot = Robot(debug=True)
# or
wheel = NZero("TheWheel", 0x40, 1, debug=True)
```

Extending the robot class:
```python
from nzerolib import Robot

class CleaningBot(Robot):
    def __init__(self, *args, **kwargs):
        super(CleaningBot, self).__init__(*args, **kwargs)
        # instantiate more devices
        self.vacuum = NZero("VacuumCleaner", 0x42, 1)

    def vacuum_clean(self):
        # ...
    def mop_floor(self):
        # ...
```

Controling the Robot with the keyboard:
```python
from nzerolib import Robot, KeyboardDriver
# the robot class has a method, just call it
bot.keyboard_drive()

# but you can also instantiate a new robot and drive like this
keyb = KeyboardDriver(bot)
keyb.drive()
```

Look for more examples at the "demo" directory.

This software is based on the amazing work of Justine Haupt, if you are building a robot, take a look at the [products on her online store](https://skysedge.com/). 

WARNING: I don't have a NearZero nor even a robot. So I can't test it. But seems to work. :) Please report any issues.
