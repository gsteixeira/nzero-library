
#I2C_M_IGNORE_NAK = 1

class DummyI2CDevice(object):
    """ A dummy i2c device for development and debug
        #pylibi2c.I2CDevice('/dev/i2c-1', 0x40)
    """
    last_command = None
    def __init__(self, dev_i2c, address):
        """ initialize """
        self.dev_i2c = dev_i2c
        self.address = address

    def write(self, *args, **kwargs):
        """ got a write call, print data to screen """
        self.last_addr = args[0]
        self.last_command = args[1]
        print("i2c: ", self.address, args[1])

    def read(self, *args, **kwargs):
        """ Read odometry TODO: to be implemented """
        print("i2c read: ", self.last_command)
        return self.last_command
