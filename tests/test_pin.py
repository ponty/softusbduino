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
    
def test_pin_nr():
    pin = dev.pin(8)
    
    eq_(pin.nr, 8)
    eq_(pin.nrAnalog, None)
   
    pin = dev.pin(14)
    eq_(pin.nr, 14)
    eq_(pin.nrAnalog, 0)
    
    pin = dev.pinAnalog(1)
    eq_(pin.nr, 15)
    eq_(pin.nrAnalog, 1)

    pin = dev.pin('D9')
    eq_(pin.nr, 9)
    eq_(pin.nrAnalog, None)

    pin = dev.pin('A2')
    eq_(pin.nr, 16)
    eq_(pin.nrAnalog, 2)
    
def test_dig():
    pin = dev.pin(8)
    pin.mode = OUTPUT
    
    pin.dig_out = 0
    eq_(pin.dig_out, 0)

    pin.dig_out = 1
    eq_(pin.dig_out, 1)

    pin.dig_out = 0
    eq_(pin.dig_out, 0)

def test_dig2():
    pin = dev.pin(8)
    pin.mode = INPUT

    pin.dig_out = 1
    eq_(pin.dig_out, 1)
    eq_(pin.mode, OUTPUT)
     
def test_an():
    pin = dev.pin('A0')
    pin.mode = INPUT
    print pin.an_in 
    print pin.analogRead() 

#    pin = dev.pin('A0')
#    pin.mode = OUTPUT
#    eq_(pin.an_in, None)
    
#    pin = dev.pin('D8')
#    pin.mode = INPUT
#    eq_(pin.an_in, None)
    
    
def test_pwm_out():
    pin = dev.pin('D9')
    pin.mode = INPUT
    pin.pwm_out = 11
    eq_(pin.mode, OUTPUT)
    pin.mode = INPUT
    

def test_pinMode2():
    pin = dev.pin(8)

    dev.registers.DDRB = 0
    eq_(dev.registers.DDRB, 0)
    eq_(pin.mode, INPUT)
    pin.mode = OUTPUT   
    eq_(pin.mode, OUTPUT)
    eq_(dev.registers.DDRB, 1)
    
    dev.reset()
    eq_(pin.mode, INPUT)
    
def test_pwm():
    pin = dev.pin(8)
    eq_(pin.pwm_available, False)
    eq_(pin.pwm_frequency, None)
    eq_(pin.timer_register_name, None)
    
    pin = dev.pin(9)
    eq_(pin.pwm_available, True)
    eq_(pin.timer_register_name, 'TCCR1B')

    eq_(pin.divisors_available, [1, 8, 64, 256, 1024])
    
    dev.registers.TCCR1B = 3
    eq_(dev.registers.TCCR1B, 3)
    
    print pin.divisor
    eq_(int(pin.pwm_frequency), 610)
    
    pin.pwm_frequency = 38
    eq_(int(pin.pwm_frequency), 38)
    eq_(dev.registers.TCCR1B, 5)
    
#    pin.pwm_frequency = 4882
    dev.registers.TCCR1B = 2
    eq_(int(pin.pwm_frequency), 4882)
    eq_(dev.registers.TCCR1B, 2)

    dev.registers.TCCR1B = 3
    eq_(dev.registers.TCCR1B, 3)


def test_pullup():
    pin = dev.pin(8)
    eq_(pin.pullup, False)
    
    pin.mode = OUTPUT
    eq_(pin.mode, OUTPUT)
    eq_(pin.pullup, False)
    pin.pullup = True
    eq_(pin.pullup, True)

    pin.mode = INPUT
    eq_(pin.mode, INPUT)
    eq_(pin.pullup, True)
