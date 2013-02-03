from nose.tools import eq_, ok_
from softusbduino.arduino import Arduino
from softusbduino.registers import RegisterError
from util import exc_

dev = None


def setup():
    global dev
    dev = Arduino()
    dev.pins.reset()


def teardown():
    global dev
    dev.pins.reset()


def test_registers():
    eq_(dev.registers is dev.registers, True)

    eq_(dev.registers.exists('DDRB'), True)
    eq_(dev.registers.exists('xDDRB'), False)

    eq_(dev.registers.read_value('DDRB'), 0)

    dev.registers.write_value('DDRB', 5)
    eq_(dev.registers.read_value('DDRB'), 5)
    dev.registers.write_value('DDRB', 0)

    eq_(dev.registers.address('DDRB'), 0x24)

    exc_(RegisterError, dev.registers.read_value, ('xx'))
    exc_(RegisterError, dev.registers.write_value, ('xx'), 0)
    exc_(RegisterError, dev.registers.address, ('xx'))


def test_dic():
    d = dev.registers.as_dict()
    eq_(d['DDRB'], 0)
    ok_(len(d) > 20)


def test_register():
    eq_(dev.register('DDRB') is dev.register('DDRB'), True)

    DDRB = dev.register('DDRB')
    DDRX = dev.register('DDRX')

    eq_(DDRB.name, 'DDRB')

    eq_(DDRB.exists, True)
    eq_(DDRX.exists, False)

    eq_(DDRB.read_value(), 0)

    DDRB.write_value(5)
    eq_(DDRB.read_value(), 5)
    eq_(DDRB.value, 5)
    DDRB.value += 1
    eq_(DDRB.value, 6)
    DDRB.value = 0

    eq_(DDRB.address, 0x24)

    exc_(RegisterError, DDRX.read_value)
    exc_(RegisterError, DDRX.write_value, 0)
    exc_(RegisterError, lambda: DDRX.address)


def test_16bit():
    ICR1 = dev.register('ICR1')

    ICR1.value = 55
    eq_(ICR1.value, 55)

    ICR1.value = 555
    eq_(ICR1.value, 555)

    ICR1.value = 5555
    eq_(ICR1.value, 5555)

    ICR1.value = 55555
    eq_(ICR1.value, 55555)


def test_size():
    ICR1 = dev.register('ICR1')
    DDRB = dev.register('DDRB')

    eq_(ICR1.size, 2)
    eq_(DDRB.size, 1)


def test_register_proxy():

    DDRB = dev.register('DDRB')
    eq_(DDRB.read_value(), 0)
    eq_(dev.registers.proxy.DDRB, 0)

    DDRB.write_value(5)
    eq_(DDRB.read_value(), 5)
    eq_(dev.registers.proxy.DDRB, 5)

    DDRB.value += 1
    eq_(DDRB.value, 6)
    eq_(dev.registers.proxy.DDRB, 6)

    DDRB.value = 0
