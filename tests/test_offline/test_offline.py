from nose.tools import eq_
from softusbduino.ser import int16_p

def test():
    eq_(int16_p(0xABCD),[0xCD,0xAB])










