from nose.tools import eq_
from softusbduino.arduino import Arduino

dev = None
def setup():
    global dev
    dev = Arduino()
    dev.reset()
    
def teardown():
    global dev
    dev.reset()
    
    
    
    
def test_read():
    print dev.defines
    print dev.registers.dump()
    print dev.productName
    print dev.manufacturer


def test_defines():
    print dev.defines
    eq_(dev.defines.A0, 14)
    eq_(dev.defines.ARDUINO, 22)
    eq_(dev.defines.MAGIC_NUMBER, 42)
    eq_(dev.defines.F_CPU, 20000000)
    
    eq_(dev.defines.dump()['A0'], 14)

    for x in dev.defines.dump():
        assert x.strip(), 'empty define:-->%s<--'%x
