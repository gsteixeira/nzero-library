# This show the basic NearZero operation
from nzerolib import NZero

# WARNING: debug mode won't write to i2c, just print to the screen
DEBUG = True

if __name__ == "__main__":
    #------------ INSTANTIATE AND START THE JOINTS -----------------
    LeftWheel = NZero("LeftWheel", 0x40, 1, debug=DEBUG)

    #-----------MAKE THE NEARZERO DO THINGS-----------------------------
    velocity = 30    #define velocity [unitless]
    current = 20     #define current [mA]
    LeftWheel.write('v', velocity, current)    #write the commands

