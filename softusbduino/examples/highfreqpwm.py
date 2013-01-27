from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
from softusbduino.const import OUTPUT


@entrypoint
def main():
    mcu = Arduino()
    mcu.pin(9).mode = OUTPUT
    mcu.pin(9).write_digital_out(1)
    pwm = mcu.pin(9).pwm
    pwm.set_high_freq_around(10000)
    print 'real frequency=', pwm.read_frequency()
