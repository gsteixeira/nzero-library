import sys
import termios
import tty
import pylibi2c

class NZero(object):
    """ NearZero interface library """

    def __init__(self, name, address, channel,
                 i2c_dev='/dev/i2c-0', delay=10, page_bytes=16, debug=False):
        """ Initialize a NearZero device
            :param name str: the name of the controled motor (eg. Wheel) 
            :param address hex: address of the NearZero device (eg. 0x40)
            :param channem str: the channel in the board. 1 or 2
            :param debug bool: dummy mode for debug
        """
        self.name = name    
        self.address = address  
        self.channel = str(channel)
        self.debug = debug
        if not self.debug:
            self.device = pylibi2c.I2CDevice(i2c_dev, self.address)
            self.device.flags = pylibi2c.I2C_M_IGNORE_NAK
        else:
            from nzerolib import dummy_i2c
            self.device = dummy_i2c.DummyI2CDevice(i2c_dev, self.address)
            self.device.flags = None
        self.device.delay = delay
        self.device.page_bytes = page_bytes

    def write(self, mode, speed, current):
        """ send data to the NearZero interface
            :param mode str: (v, p) mode of motor, Velocity or Position.
            :param speed int: the speed of the motor.
            :param current int: the current applied to the motor.
        """
        f_speed   = '{:+06d}'.format(speed)
        f_current = '{:05d}'.format(current)
        i2c_out = ''.join([self.channel, mode, f_speed, 'c', f_current])
        self.device.write(0x0, i2c_out)


class Robot(object):
    """ This class controls the Robot
    """
    # initial speeds
    vel_forward = 0
    vel_sideways = 0
    # head
    head_yaw = 0
    head_pitch = 0
    head_roll = 0
    
    def __init__(self,
                 wheel_dev='/dev/i2c-0', wheel_addr=0x40,
                 head_dev='/dev/i2c-0', head_addr=0x41,
                 debug=False, verbose=False):
        """  INSTANTIATE THE JOINTS
        :param wheel_dev str: device of NZ for wheels
        :param wheel_addr hex: address of NZ for wheels
        :param head_dev str: device of NZ for head
        :param head_addr hex: address of NZ for head
        :param debug bool: use dummy i2c device
        :param verbose bool: print info
        """
        self.LeftWheel = NZero("LeftWheel", wheel_addr, "1", 
                               i2c_dev=wheel_dev, debug=debug)
        self.RightWheel = NZero("RightWheel", wheel_addr, "2",
                                i2c_dev=wheel_dev, debug=debug)
        self.HeadYaw = NZero("HeadYaw", head_addr, "1",
                             i2c_dev=head_dev, debug=debug)
        self.HeadPitch = NZero("HeadPitch", head_addr, "2",
                               i2c_dev=head_dev, debug=debug)
        self.debug = debug
        self.verbose = verbose

    def go_forward(self):
        """ increment forward velocity """
        self.vel_forward += 20
        self.move()
    
    def go_backwards(self):
        """ s = increment backward velocity """
        self.vel_forward -= 20
        self.move()
    
    def go_left(self):
        """ a = increment left steering """
        self.vel_sideways -= 10
        self.move()

    def go_right(self):
        """ d = increment right steering """
        self.vel_sideways += 10
        self.move()

    def stop_move(self):
        """ x = freeze """
        self.vel_forward = 0
        self.vel_sideways = 0
        self.move()
    
    def move_ahead(self, speed):
        """ move the robot ahead of backwards giving a fixed speed """
        self.vel_forward = speed
        self.move()
    
    def move_sideways(self, speed):
        """ rotate giving a fixed speed """
        self.vel_sideways = speed
        self.move()

    ### Head ##
    def head_up(self):
        """ i = point head up """
        self.head_pitch += 150
        self.HeadPitch.write('p', self.head_pitch, 50)

    def head_down(self):
        """ m = point head down """
        self.head_pitch -= 150
        self.HeadPitch.write('p', self.head_pitch, 50)

    def head_left(self):
        """ j = point head left """
        self.head_yaw -= 500
        self.HeadYaw.write('p', self.head_yaw, 50)

    def head_right(self):
        """ k = point head right """
        self.head_yaw += 500
        self.HeadYaw.write('p', self.head_yaw, 50)
    
    def head_roll_left(self):
        """ head_roll_left """
        self.head_roll -= 100
        self.HeadRoll.write('p', self.head_roll, 50)

    def head_roll_right(self):
        """ head_roll_right """
        self.head_roll += 100
        self.HeadRoll.write('p', self.head_roll, 10)
        
    def head_stop(self):
        """ o = head motors off """
        self.HeadPitch.write('p', self.head_pitch, 0)
        self.HeadYaw.write('p', self.head_yaw, 0)
        self.HeadRoll.write('p', self.head_roll, 0)

    def move(self):
        """ Moves the robot.
            This function takes in self.vel_forward and self.vel_sideways 
            and calculates the differential drive velocity for each wheel 
            and writes it to each wheel
        """
        vel_left = -1 * (self.vel_forward + self.vel_sideways)
        vel_right = self.vel_forward - self.vel_sideways
        current_left = 1 * int(abs(vel_left))
        current_right = 1 * int(abs(vel_right))
        if vel_left == 0:
            current_left = 0
        if vel_right == 0:
            current_right = 0
        self.LeftWheel.write('v', vel_left, current_left)
        self.RightWheel.write('v', vel_right, current_right)
        if self.verbose:
            msg = ''.join([
                "current_left=", str(current_left), "\n",
                "current_right=", str(current_right), "\n",
                "vel_left=", str(vel_left), "\n",
                "vel_right=", str(vel_right),
                ])
            print(msg)

    def keyboard_drive(self):
        """ drives the robot with the keyboard """
        driver = KeyboardDriver(self)
        driver.drive()

    def print_odometry(self):
        """ show robot status TODO to be implemented """
        odometry = self.LeftWheel.device.read(0x0, 12)
        print("odometry", odometry)


class KeyboardDriver(object):
    def __init__(self, robot):
        self.robot = robot

    def drive(self):
        """ drives the robot with the keyboard """
        def getch():
            """ get a char from keyboard. this function is only used here """
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
        
        self.print_help()
        commands = {
            'w': self.robot.go_forward,
            's': self.robot.go_backwards,
            'a': self.robot.go_left,
            'd': self.robot.go_right,
            'x': self.robot.stop_move,
            # head
            'i': self.robot.head_up,
            'm': self.robot.head_down,
            'j': self.robot.head_left,
            'k': self.robot.head_right,
            'h': self.robot.head_roll_left,
            'l': self.robot.head_roll_right,
            'o': self.robot.head_stop,
            
            'u': self.print_help,
            }
        char = None
        while char != 'q':
            char = getch()
            func = commands.get(char, None)
            if func:
                func()
        self.robot.stop_move()

    def print_help(self):
        text = """
            w = increment forward velocity
            s = increment backward velocity
            a = increment left steering
            d = increment right steering
            x = freeze
            
            i = point head up
            m = point head down
            j = point head left
            k = point head right
            o = head motors off
            
            u = usage
            q = quit
        """
        print(text)
