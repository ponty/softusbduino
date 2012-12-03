from softusbduino.check.dump import usbdump
from softusbduino.examples import simple


def test_usbdump():
    usbdump()
    simple.main()
