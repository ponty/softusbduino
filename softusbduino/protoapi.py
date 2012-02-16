from const import *
from arduino import Arduino
from delay import *

board = Arduino()
A0 = board.defines.A0
A1 = A0 + 1
A2 = A0 + 2
A3 = A0 + 3
A4 = A0 + 4
A5 = A0 + 5

analogRead = board.analogRead
analogWrite = board.analogWrite
analogReference = board.analogReference
digitalWrite = board.digitalWrite
digitalRead = board.digitalRead
pinMode= board.pinMode
digitalPinToBitMask = board.digitalPinToBitMask
digitalPinToPort= board.digitalPinToPort
portModeRegister=board.portModeRegister

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
    








