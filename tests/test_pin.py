from nose.tools import eq_, ok_
from softusbduino.arduino import Arduino
from softusbduino.const import *
from test_vcc import ok_vcc

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
    
    pin.write_digital(1)
    eq_(dev.pins.read_digital(8), 1)
    eq_(pin.read_digital(), 1)
    eq_(pin.digital, 1)
    eq_(dev.pins.read_digital_out(8), 1)
    eq_(pin.read_digital_out(), 1)
    eq_(pin.digital_out, 1)
    eq_(dev.pins.read_digital_in(8), None)
    eq_(pin.read_digital_in(), None)
    eq_(pin.digital_in, None)
    

    pin.write_digital(0)
    eq_(dev.pins.read_digital(8), 0)
    eq_(pin.read_digital(), 0)
    eq_(pin.digital, 0)
    eq_(dev.pins.read_digital_out(8), 0)
    eq_(pin.read_digital_out(), 0)
    eq_(pin.digital_out, 0)
    eq_(dev.pins.read_digital_in(8), None)
    eq_(pin.read_digital_in(), None)
    eq_(pin.digital_in, None)


    pin.write_mode(INPUT)
    pin.write_pullup(True)
    eq_(dev.pins.read_digital(8), 1)
    eq_(pin.read_digital(), 1)
    eq_(pin.digital, 1)
    eq_(dev.pins.read_digital_out(8), None)
    eq_(pin.read_digital_out(), None)
    eq_(pin.digital_out, None)
    eq_(dev.pins.read_digital_in(8), 1)
    eq_(pin.read_digital_in(), 1)
    eq_(pin.digital_in, 1)

    pin.digital_out =(1)
    eq_(pin.mode, OUTPUT)

def ok_an(x, value=None):     
    print x 
    ok_(x in range(1024)) 
    if value is not None:
        eq_(x, value)
    
def test_an():
    pin = dev.pin('A0')
    pin.mode = INPUT
    ok_an(pin.read_analog()) 
    ok_an(dev.pins.read_analog(14)) 

    pin.write_pullup(True)
    ok_an(dev.pins.read_analog(14), 1023) 
    ok_an(pin.read_analog(), 1023) 
    ok_an(pin.analog, 1023) 

    ok_an(dev.pins.read_analog_obj(14).value, 1023) 
    ok_an(pin.read_analog_obj().value, 1023) 
    ok_an(pin.analog_obj.value, 1023) 
    
    ok_vcc(pin.analog_obj.voltage) 
    
#    pin = dev.pin('A0')
#    pin.mode = OUTPUT
#    eq_(pin.an_in, None)
    
#    pin = dev.pin('D8')
#    pin.mode = INPUT
#    eq_(pin.an_in, None)
    
    
def test_mode():
    pin = dev.pin(8)

    dev.reset()
    
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
    dev.reset()
    eq_(pin.mode, INPUT)
    


def test_pullup():
    pin = dev.pin(8)
#    eq_(pin.pullup, False)
    
    pin.write_mode(OUTPUT)
    eq_(pin.mode, OUTPUT)
#    eq_(pin.pullup, False)
    pin.write_pullup(True)
#    eq_(pin.pullup, True)

    pin.write_mode(INPUT)
    eq_(pin.mode, INPUT)
#    eq_(pin.pullup, True)

def test_memoize():
    assert dev.pin(8) is dev.pin(8)
    assert dev.pin(1) is dev.pin('D1')
    assert dev.pin(14) is dev.pin('A0')
    

def test_usb_pin():
    eq_(dev.pins.usb_minus_pin, 4)
    eq_(dev.pins.usb_plus_pin, 2)
    
    eq_(dev.pin(0).is_usb_plus, False)
    eq_(dev.pin(0).is_usb_minus, False)
    

    eq_(dev.pin(2).is_usb_plus, True)
    eq_(dev.pin(2).is_usb_minus, False)

    eq_(dev.pin(4).is_usb_plus, False)
    eq_(dev.pin(4).is_usb_minus, True)


def test_pin_range():
    eq_(dev.pins.count, 20)
    eq_(dev.pins.count_analog, 6)
    eq_(dev.pins.count_digital, 14)

    eq_(dev.pins.range_all, range(0, 20))
    eq_(dev.pins.range_analog, range(14, 20))
    eq_(dev.pins.range_digital, range(0, 14))
    
    
