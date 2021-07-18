# Drive the robot with the keyboard
from nzerolib import Robot
from time import sleep

# WARNING: debug mode won't write to i2c, just print to the screen
DEBUG = True

if __name__ == "__main__":
    bot = Robot(verbose=True, debug=DEBUG)
    bot.keyboard_drive()
