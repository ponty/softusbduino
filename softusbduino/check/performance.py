from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
import time


def measure(mcu, n, f):
    start = time.time()
    for x in range(n):
        cmd = 'mcu.' + f
        try:
            exec cmd
        except:
            print cmd
            raise
    dt = time.time() - start
    print '%-35s %8.2f ms per call, %5.0f call per second' % (f, 1000.0 * dt / n, 1.0 / dt * n)


@entrypoint
def main(n=100):
    mcu = Arduino()

    print 'performance test'
    print 'n=', n
    print
    measure(mcu, n, 'pins.read_analog(0)')
    measure(mcu, n, 'pins.write_mode(8,0)')
    measure(mcu, n, 'pins.read_digital(8)')
#    measure(mcu,n, 'digitalPinToBitMask(0)')
#    measure(mcu,n, 'digitalPinToPort(0)')
#    measure(mcu,n, 'portModeRegister(0)')

    # defines
    measure(mcu, n, 'defines.value("__TIME__")')
    measure(mcu, n, 'defines.exists("__TIME__")')
    measure(mcu, n, 'defines.exists("xx")')
    measure(mcu, n, 'define("A0")')
#    measure(mcu,n, 'define("xx")')

    # registers
    measure(mcu, n, 'registers.read_value("DDRB")')
    measure(mcu, n, 'registers.exists("DDRB")')
    measure(mcu, n, 'registers.exists("xx")')
    measure(mcu, n, 'register("DDRB").value')
    measure(mcu, n, 'register("DDRB").read_value()')
    measure(mcu, n, 'register("DDRB").exists')
    measure(mcu, n, 'register("xx").exists')

    # vcc
    measure(mcu, n, 'vcc.voltage')
    measure(mcu, n, 'vcc.read_voltage()')
    measure(mcu, n, 'read_vcc()')

    measure(mcu, n, 'pins.count')
    measure(mcu, n, 'pins.usb_minus_pin')
    measure(mcu, n, 'pins.usb_plus_pin')
    measure(mcu, n, 'firmware_test()')
#    measure(mcu,n, 'pin("A0").analog_in().value')

    measure(mcu, n, 'pins.read_mode(0)')
    measure(mcu, n, 'reset()')
