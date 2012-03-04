from const import *
from arduino import Arduino
from delay import *

mcu = Arduino()
A0 = mcu.defines.value('A0')
A1 = A0 + 1
A2 = A0 + 2
A3 = A0 + 3
A4 = A0 + 4
A5 = A0 + 5

analogRead = mcu.pins.read_analog
analogWrite = mcu.pwm.write_value
analogReference = mcu.lowlevel_pins.analogReference
digitalWrite = mcu.pins.write_digital
digitalRead = mcu.pins.read_digital
pinMode= mcu.pins.write_mode
digitalPinToBitMask = mcu.lowlevel_pins.digitalPinToBitMask
digitalPinToPort= mcu.lowlevel_pins.digitalPinToPort
portModeRegister=mcu.lowlevel_pins.portModeRegister

class Sketch(object):
    def __init__(self, setup, loop):
        self.setup = setup
        self.loop = loop
        
    def run(self):
        self.setup()
        while 1:
            self.loop()

def Serial_begin(x):
    pass
def Serial_print(x):
    print x,
def Serial_println(x):
    print x
    
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    







