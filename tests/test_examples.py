from softusbduino.check import performance, delay, dump
from softusbduino.examples import simple


def test_usbdump():
    dump.usbdump()


def test_simple():
    simple.main()


def test_perf():
    performance.main()

# very slow
#def test_delay():
#    delay.main()
