from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
from softusbduino.const import OUTPUT



@entrypoint
def main():
    mcu = Arduino()
    p = mcu.pin(5)
    p.write_mode(OUTPUT)
    p.pwm.write_value(128)
    print mcu.counter.run(1)

