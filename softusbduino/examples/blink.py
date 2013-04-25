from softusbduino.const import OUTPUT
from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
import time


@entrypoint
def main(
    pin='D13',
    t=0.1,
):
    mcu = Arduino()
    p=mcu.pin(pin)
    p.write_mode(OUTPUT)
    x=0
    while 1:
        x=1-x
        p.write_digital_out(x)
        time.sleep(t)
