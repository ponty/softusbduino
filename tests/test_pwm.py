from nose.tools import eq_
from softusbduino.arduino import Arduino
from softusbduino.const import *
from config import F_CPU

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
    
    frequencies=[F_CPU/2**9, 
                 F_CPU/2**12, 
                 F_CPU/2**15, 
                 F_CPU/2**17, 
                 F_CPU/2**19, 
                 ]
    eq_(pwm.frequencies_available(9), frequencies)
    eq_(pin9.pwm.frequencies_available, frequencies)

    TCCR1B.value = 3
    eq_(TCCR1B.value, 3)
    
    eq_(pwm.read_divisor(9), 2**6)
    eq_(pin9.pwm.read_divisor(), 2**6)
    eq_(pin9.pwm.divisor, 2**6)
    eq_(pwm.read_frequency(9), F_CPU/2**15)
    eq_(pin9.pwm.read_frequency(), F_CPU/2**15)
    eq_(pin9.pwm.frequency, F_CPU/2**15)
    
    pwm.write_frequency(9, int(F_CPU/2**19))
    eq_(pwm.read_frequency(9), F_CPU/2**19)
    eq_(TCCR1B.value, 5)
    
    TCCR1B.value = 2
    eq_(pwm.read_divisor(9), 2**3)
    eq_(pin9.pwm.read_divisor(), 2**3)
    eq_(pin9.pwm.divisor, 2**3)
    eq_(pwm.read_frequency(9), F_CPU/2**12)
    eq_(pin9.pwm.read_frequency(), F_CPU/2**12)
    eq_(pin9.pwm.frequency, F_CPU/2**12)
    eq_(TCCR1B.value, 2)

    pin9.pwm.divisor = 2**10
    eq_(pwm.read_divisor(9), 2**10)
    eq_(pin9.pwm.read_divisor(), 2**10)
    eq_(pin9.pwm.divisor, 2**10)
    eq_(pwm.read_frequency(9), F_CPU/2**19)
    eq_(pin9.pwm.read_frequency(), F_CPU/2**19)
    eq_(pin9.pwm.frequency, F_CPU/2**19)
    eq_(TCCR1B.value, 5)

    
    pin9.pwm.write_frequency(F_CPU/2**9)
    eq_(pwm.read_frequency(9), F_CPU/2**9)
    eq_(TCCR1B.value, 1)

    pin9.pwm.frequency = F_CPU/2**17
    eq_(pwm.read_frequency(9), F_CPU/2**17)
    eq_(TCCR1B.value, 4)

    TCCR1B.value = 3
    eq_(TCCR1B.value, 3)

def test_value():
    pwm = dev.pwm
    pin9 = dev.pin(9)
    
    pwm.write_value(9, 55)
    pin9.pwm.write_value(45)
