from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
from softusbduino.const import OUTPUT


@entrypoint
def main(loop=1):
    mcu = Arduino()
#    p = mcu.pin(5)
#    print p.pwm.frequencies_available
#    p.write_mode(OUTPUT)
#    p.pwm.write_value(128)
#    p.pwm.frequency = 1220
    with mcu.counter:
        if loop:
            while 1:
                print mcu.counter.run(1)
        else:
            print mcu.counter.run(1)
