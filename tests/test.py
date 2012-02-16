from nose.tools import eq_
from softusbduino.arduino import Arduino, OUTPUT, INPUT
from util import exc_

dev = None
def setup():
    global dev
    dev = Arduino()
    dev.reset()
    
def teardown():
    global dev
    dev.reset()
    
def test_pinMode():
    eq_(dev.readPinMode(8), INPUT)
    dev.pinMode(8, OUTPUT)
    eq_(dev.readPinMode(8), OUTPUT)
    dev.pinMode(8, INPUT)
    eq_(dev.readPinMode(8), INPUT)
    
def test_defs():
    eq_(dev.idVendor, 0x16c0)
    eq_(dev.idProduct, 0x05df)
 
    eq_(dev.usbMinusPin, 4)
    eq_(dev.usbPlusPin, 2)

    eq_(dev.pinCount, 20)

    eq_(dev.pinRange(), range(0, 20))
    eq_(dev.pinRange('digital'), range(0, 14))
    eq_(dev.pinRange('analog'), range(14, 20))
    
    eq_(dev.defines.A0, 14)
    


def test_vcc():
    x = dev.vcc
    assert 4 < x < 5, x
    
    
    
    
def test_reg():
    dev.reset()
    dev.registers.DDRB=1
    
    eq_(1, dev.registers.DDRB)
    exc_(AttributeError, lambda :dev.registers.DDRBxxx)
    
    reg=dev.register('DDRB')
    eq_(True, reg.available)
    eq_(1, reg.value)
    reg.value=2
    eq_(2, reg.value)
    eq_(36, reg.address)
    
    # known but missing
    eq_(None, dev.register('DDRA'))

    # unknown
    try:
        dev.register('DDRAxxx')
        assert 0
    except KeyError:
        pass




