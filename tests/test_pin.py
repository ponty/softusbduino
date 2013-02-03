from measurement import AnalogIn
from nose.tools import eq_, ok_
from softusbduino.arduino import Arduino
from softusbduino.const import *
from test_vcc import ok_vcc
from util import exc_
import time
from config import config

dev = None


def setup():
    global dev
    dev = Arduino()
    dev.pins.reset()


def teardown():
    global dev
    dev.pins.reset()


def test_pin_nr():
    pin = dev.pin(8)

    eq_(pin.nr, 8)
    eq_(pin.nr_analog, None)

    pin = dev.pin(14)
    eq_(pin.nr, 14)
    eq_(pin.nr_analog, 0)

    pin = dev.pin('A1')
    eq_(pin.nr, 15)
    eq_(pin.nr_analog, 1)

    pin = dev.pin('D9')
    eq_(pin.nr, 9)
    eq_(pin.nr_analog, None)

    pin = dev.pin('A2')
    eq_(pin.nr, 16)
    eq_(pin.nr_analog, 2)


def test_is():
    eq_(dev.pin(8).is_digital, True)
    eq_(dev.pin(8).is_analog, False)
    eq_(dev.pin('A2').is_digital, False)
    eq_(dev.pin('A2').is_analog, True)


def test_name():
    eq_(dev.pin(8).name, 'D8')
    eq_(dev.pin('D8').name, 'D8')
    eq_(dev.pin(15).name, 'A1')
    eq_(dev.pin('A2').name, 'A2')


def test_dig():
    pin = dev.pin(8)
    pin.reset()

    pin.write_mode(OUTPUT)

    pin.write_digital_out(1)
#    eq_(dev.pins.read_digital(8), 1)
#    eq_(pin.read_digital(), 1)
#    eq_(pin.digital, 1)
    eq_(dev.pins.read_digital_out(8), 1)
    eq_(pin.read_digital_out(), 1)
#    eq_(pin.digital_out, 1)
#    eq_(dev.pins.read_digital_in(8), None)
#    eq_(pin.read_digital_in(), None)
#    eq_(pin.digital_in, None)

    pin.write_mode(INPUT)
    pin.write_mode(OUTPUT)
#    eq_(dev.pins.read_digital_out(8), 1)

    pin.write_digital_out(0)
#    eq_(dev.pins.read_digital(8), 0)
#    eq_(pin.read_digital(), 0)
#    eq_(pin.digital, 0)
    eq_(dev.pins.read_digital_out(8), 0)
    eq_(pin.read_digital_out(), 0)
#    eq_(pin.digital_out, 0)
#    eq_(dev.pins.read_digital_in(8), None)
#    eq_(pin.read_digital_in(), None)
#    eq_(pin.digital_in, None)

    pin.write_mode(INPUT)
    pin.write_mode(OUTPUT)
    eq_(dev.pins.read_digital_out(8), 0)

    pin.write_mode(INPUT)
    pin.write_pullup(True)
#    eq_(dev.pins.read_digital(8), 1)
#    eq_(pin.read_digital(), 1)
#    eq_(pin.digital, 1)
#    eq_(dev.pins.read_digital_out(8), None)
#    eq_(pin.read_digital_out(), None)
#    eq_(pin.digital_out, None)
    eq_(dev.pins.read_digital_in(8), 1)
    eq_(pin.read_digital_in(), 1)
    eq_(pin.digital_in, 1)

#    pin.digital_out = (1)
#    eq_(pin.mode, OUTPUT)


def ok_an(x, pullup=False):
    print x
    ok_(x in range(1024))
    if pullup:
        # TODO: why can the analog value with pullup be so low?
        ok_(x > 900)


def test_an():
    pin = dev.pin('A0')
    pin.mode = INPUT
    ok_an(pin.read_analog())
    ok_an(dev.pins.read_analog(14))

    pin.write_pullup(True)

    ok_an(dev.pins.read_analog(14), pullup=True)
    ok_an(pin.read_analog(), pullup=True)
    ok_an(pin.analog, pullup=True)

#    ok_an(dev.pins.read_analog_obj(14).value, pullup=True)
    ok_an(AnalogIn(pin).read().value, pullup=True)
#    ok_an(pin.analog_obj.value, pullup=True)

#    ok_vcc(pin.analog_obj.voltage)

#    pin = dev.pin('A0')
#    pin.mode = OUTPUT
#    eq_(pin.an_in, None)

#    pin = dev.pin('D8')
#    pin.mode = INPUT
#    eq_(pin.an_in, None)


def test_mode():
    pin = dev.pin(8)

    dev.pins.reset()

    eq_(pin.mode, INPUT)
    eq_(pin.read_mode(), INPUT)
    eq_(dev.pins.read_mode(8), INPUT)
    eq_(dev.registers.read_value('DDRB'), 0)

    pin.write_mode(OUTPUT)
    eq_(pin.mode, OUTPUT)
    eq_(pin.read_mode(), OUTPUT)
    eq_(dev.pins.read_mode(8), OUTPUT)
    eq_(dev.registers.read_value('DDRB'), 1)

    dev.registers.write_value('DDRB', 0)
    eq_(pin.mode, INPUT)

    pin.mode = OUTPUT
    eq_(pin.mode, OUTPUT)

    dev.pins.write_mode(8, INPUT)
    eq_(pin.mode, INPUT)

    pin.mode = OUTPUT
    dev.pins.reset()
    eq_(pin.mode, INPUT)


def test_pullup():
    pin = dev.pin(8)
#    eq_(pin.pullup, False)

    pin.write_mode(OUTPUT)
    eq_(pin.mode, OUTPUT)
#    eq_(pin.pullup, False)
#    pin.write_pullup(True)
#    eq_(pin.pullup, True)

    pin.write_mode(INPUT)
    eq_(pin.mode, INPUT)
#    eq_(pin.pullup, True)
    pin.write_pullup(True)


def test_memoized():
    assert dev.pin(8) is dev.pin(8)
    assert dev.pin(1) is dev.pin('D1')
    assert dev.pin(14) is dev.pin('A0')


def test_usb_pin():
    p = config.pin_usb_plus
    m = config.pin_usb_minus
    eq_(dev.pins.usb_minus_pin, p)
    eq_(dev.pins.usb_plus_pin, m)

    eq_(dev.pin(5).is_usb_plus, False)
    eq_(dev.pin(5).is_usb_minus, False)

    eq_(dev.pin(m).is_usb_plus, True)
    eq_(dev.pin(m).is_usb_minus, False)

    eq_(dev.pin(p).is_usb_plus, False)
    eq_(dev.pin(p).is_usb_minus, True)


def test_pin_range():
    eq_(dev.pins.count, 20)
    eq_(dev.pins.count_analog, 6)
    eq_(dev.pins.count_digital, 14)

    eq_(dev.pins.range_all, range(0, 20))
    eq_(dev.pins.range_analog, range(14, 20))
    eq_(dev.pins.range_digital, range(0, 14))

    dev.pin('A5')
    exc_(ValueError, lambda: dev.pin('A6'))
    exc_(ValueError, lambda: dev.pin('D14'))

