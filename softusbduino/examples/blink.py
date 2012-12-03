from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
import time


@entrypoint
def main(
    pin='D13',
    t=0.1,
):
    mcu = Arduino()
    while 1:
        mcu.pin(pin).digital_out = not mcu.pin(pin).digital_out
        time.sleep(t)
