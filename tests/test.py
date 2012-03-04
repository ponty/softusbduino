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
    
    
def test_defs():
    eq_(dev.usb.id_vendor, 0x16c0)
    eq_(dev.usb.id_product, 0x05df)
 
 
    
    
    




