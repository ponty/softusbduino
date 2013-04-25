from softusbduino.arduino import Arduino
from softusbduino.check import performance, delay, dump, vcc, version, watchdog
from softusbduino.examples import simple
import sys


def setup():
    global dev
    dev = Arduino()
    dev.pins.reset()


def teardown():
    global dev
    dev.pins.reset()


def test_usbdump():
    dump.usbdump()


def test_simple():
    simple.main()


def test_perf():
    performance.main()


def test_vcc():
    vcc.main()


def test_version():
    version.main()


def test_watchdog():
    watchdog.main()

# very slow
def test_delay():
#     if (sys.version_info < (2, 6, 0)):
    if 1:
        from nose.plugins.skip import SkipTest
        raise SkipTest    
    delay.main()
