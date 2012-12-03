from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
import time


@entrypoint
def main(
    t=0.1,
):
    mcu = Arduino()
    while 1:
        for x in mcu.pins.range_analog:
            pin = mcu.pin(x)
            print '%s:%s' % (pin.name, pin.read_analog()),
        print
        time.sleep(t)
