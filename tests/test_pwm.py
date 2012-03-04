from nose.tools import eq_
from softusbduino.arduino import Arduino
from softusbduino.const import *

dev = None
def setup():
    global dev
    dev = Arduino()
    dev.reset()
    
def teardown():
    global dev
    dev.reset()
    
#def test_pwm_out():
#    pin = dev.pin('D9')
#    pin.write_mode(INPUT)
#    pin.pwm_out = 11
#    eq_(pin.mode(), OUTPUT)
#    pin.write_mode(INPUT)
    

def test_pwm():
    pwm = dev.pwm
    pin9 = dev.pin(9)
    TCCR1B = dev.register('TCCR1B')
    
    eq_(pwm.available(8), False)
    
    eq_(pwm.available(9), True)
    eq_(pin9.pwm.available, True)
    eq_(pwm.timer_register_name(9), 'TCCR1B')
    eq_(pin9.pwm.timer_register_name, 'TCCR1B')
    
    eq_(pwm.base_divisor(9), 512)
    eq_(pin9.pwm.base_divisor, 512)
    
    eq_(pwm.divisors_available(9), [1, 8, 64, 256, 1024])
    eq_(pin9.pwm.divisors_available, [1, 8, 64, 256, 1024])
    
    eq_(pwm.frequencies_available(9), [39062.5, 4882.8125, 610.3515625, 152.587890625, 38.14697265625])
    eq_(pin9.pwm.frequencies_available, [39062.5, 4882.8125, 610.3515625, 152.587890625, 38.14697265625])

    TCCR1B.value = 3
    eq_(TCCR1B.value, 3)
    
    eq_(pwm.read_divisor(9), 64)
    eq_(pin9.pwm.read_divisor(), 64)
    eq_(pin9.pwm.divisor, 64)
    eq_(int(pwm.read_frequency(9)), 610)
    eq_(int(pin9.pwm.read_frequency()), 610)
    eq_(int(pin9.pwm.frequency), 610)
    
    pwm.write_frequency(9, 38)
    eq_(int(pwm.read_frequency(9)), 38)
    eq_(TCCR1B.value, 5)
    
    TCCR1B.value = 2
    eq_(pwm.read_divisor(9), 8)
    eq_(pin9.pwm.read_divisor(), 8)
    eq_(pin9.pwm.divisor, 8)
    eq_(int(pwm.read_frequency(9)), 4882)
    eq_(int(pin9.pwm.read_frequency()), 4882)
    eq_(int(pin9.pwm.frequency), 4882)
    eq_(TCCR1B.value, 2)

    pin9.pwm.divisor = 1024
    eq_(pwm.read_divisor(9), 1024)
    eq_(pin9.pwm.read_divisor(), 1024)
    eq_(pin9.pwm.divisor, 1024)
    eq_(int(pwm.read_frequency(9)), 38)
    eq_(int(pin9.pwm.read_frequency()), 38)
    eq_(int(pin9.pwm.frequency), 38)
    eq_(TCCR1B.value, 5)

    
    pin9.pwm.write_frequency(39062)
    eq_(int(pwm.read_frequency(9)), 39062)
    eq_(TCCR1B.value, 1)

    pin9.pwm.frequency = 152
    eq_(int(pwm.read_frequency(9)), 152)
    eq_(TCCR1B.value, 4)

    TCCR1B.value = 3
    eq_(TCCR1B.value, 3)

def test_value():
    pwm = dev.pwm
    pin9 = dev.pin(9)
    
    pwm.write_value(9, 55)
    pin9.pwm.write_value(45)
