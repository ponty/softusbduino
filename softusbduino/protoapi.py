from const import *
from arduino import Arduino
from delay import *
from softusbduino.memo import memoized

#mcu = Arduino()
#A0 = mcu.defines.value('A0')
#A1 = A0 + 1
#A2 = A0 + 2
#A3 = A0 + 3
#A4 = A0 + 4
#A5 = A0 + 5

@memoized
def get_mcu():
    return Arduino()
    
def analogRead(*args):
    return get_mcu().pins.read_analog(*args)

def analogWrite(*args):
    return get_mcu().pwm.write_value(*args)
def analogReference(*args):
    return get_mcu().lowlevel_pins.analogReference(*args)
def digitalWrite(*args):
    return get_mcu().pins.write_digital_fast(*args)
def digitalRead(*args):
    return get_mcu().pins.read_digital_fast(*args)
def pinMode(*args):
    return get_mcu().pins.write_mode(*args)
def digitalPinToBitMask(*args):
    return get_mcu().lowlevel_pins.digitalPinToBitMask(*args)
def digitalPinToPort(*args):
    return get_mcu().lowlevel_pins.digitalPinToPort(*args)
def portModeRegister(*args):
    return get_mcu().lowlevel_pins.portModeRegister(*args)


class Sketch(object):
    def __init__(self, setup, loop):
        self.setup = setup
        self.loop = loop

    def run(self):
        self.setup()
        while 1:
            self.loop()


class CSerial(object):
    def begin(self, x):
        pass

    def print_(self, x):
        print x,

    def println(self, x):
        print x

Serial = CSerial()


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
