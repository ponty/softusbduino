from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
from softusbduino.const import OUTPUT
import time


@entrypoint
def dig_out():
    dev = Arduino()
    dev.reset()
    pin = dev.pin(8)
    pin.mode = OUTPUT

    pin2 = dev.pin('A0')
    while 1:
        time.sleep(0.001)
        pin.dig_out = 0
        pin2.analog_in().value
        pin.dig_out = 1
        pin2.analog_in().value
