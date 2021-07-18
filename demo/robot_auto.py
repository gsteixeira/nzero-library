# Let the robot walk on it's own
from nzerolib import Robot
from time import sleep

# WARNING: debug mode won't write to i2c, just print to the screen
DEBUG = True

if __name__ == "__main__":
    # Instantiate the robot
    bot = Robot(debug=DEBUG, verbose=True)

    # make it move
    print('The Robot will do some basic moves')
    bot.stop_move()
    bot.go_forward()
    sleep(1)
    bot.go_left()
    sleep(1)
    bot.go_right()
    sleep(1)
    bot.stop_move()

    # Speedup then slowdown
    print("Speed up")
    for i in range(0, 150, 20):
        bot.move_ahead(i)
        sleep(0.3)
    print("Slow down")
    for i in range(150, 0, -20):
        # go_forward and go_backwards have the same effect when passing speed
        bot.move_ahead(i)
        sleep(0.3)
    bot.stop_move()
