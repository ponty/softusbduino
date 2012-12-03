from nose.tools import eq_, ok_
from softusbduino.arduino import Arduino
from util import exc_

dev = None


def setup():
    global dev
    dev = Arduino()
    dev.reset()


def teardown():
    global dev
    dev.reset()


def  ok_vcc(vcc):
    print 'vcc=', vcc
    ok_(vcc < 5.5)
    ok_(vcc > 4.5)


def test_vcc():
    ok_vcc(dev.read_vcc())
    ok_vcc(dev.read_u_vcc())

    ok_vcc(dev.vcc.voltage)
    ok_vcc(dev.vcc.u_voltage)
    ok_vcc(dev.vcc.read_voltage())
    ok_vcc(dev.vcc.read_u_voltage())

    dev.vcc.voltage = 7
    eq_(dev.vcc.voltage, 7)
    dev.vcc.read_voltage()
    ok_vcc(dev.vcc.voltage)
