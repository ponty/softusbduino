from remember.memoize import memoize
from softusbduino.const import *
from softusbduino.pwmpin import PwmPinMixin
from uncertainties import ufloat
import logging
import time

log = logging.getLogger(__name__)

class RemoteVar(object):
    pin = None
    value = None
    t = None
    def __init__(self, pin):
        self.pin = pin
        self.read()

    def read(self):
        self.t = time.time()
        self.value = self._read_value()
        
        
   
class AnalogIn(RemoteVar):
    def _read_value(self):
        return self.pin._analogRead()
            
    @property
    def u_value(self):
        return ufloat((self.value, self.pin.mcu.adc_accuracy))

    @property
    def voltage(self):
        return self.u_voltage.nominal_value
    
    @property
    def u_voltage(self):
        return self.u_value / 1024.0 * self.pin.mcu.vcc.voltage

class AnalogInputValue(RemoteVar):
    pin = None
    value = None
    t = None
    def __init__(self, mcu, pin_nr):
        self.pin_nr = pin_nr
        self.mcu=mcu
        
        self.t = time.time()
        self.value=mcu.pins.read_analog(pin_nr)
            
    @property
    def u_value(self):
        return ufloat((self.value, self.mcu.adc_accuracy))

    @property
    def voltage(self):
        return self.u_voltage.nominal_value
    
    @property
    def u_voltage(self):
        return self.u_value / 1024.0 * self.mcu.vcc.voltage
    
#class Digital(RemoteVar):
#    def _read_value(self):
#        return self.pin._digitalRead()

#class PinMode(RemoteVar):
#    def _read_value(self):
#        return self.pin._readPinMode()

def pin_nr_as_int(nr, A0):
    if isinstance(nr, basestring):
        if nr[0] == 'D':
            nr = int(nr[1:])
        elif nr[0] == 'A':
            nr = int(nr[1:]) + A0
    nr = int(nr)
    return nr

class Pin(PwmPinMixin):
    def __init__(self, base, mcu, nr):
        self.base = base
        self.mcu = mcu
        self.A0 = mcu.define('A0')
        self.nr = pin_nr_as_int(nr, self.A0)
        
    @property
    def is_digital(self):
        return self.nr < self.A0
    
    @property
    def is_analog(self):
        return not self.is_digital

    @property
    def name(self):
        if self.is_digital:
            return 'D%s' % self.nr
        else:
            return 'A%s' % self.nr_analog
            
            
    @property
    def nr_analog(self):
        x = self.nr - self.A0
        if x >= 0:
            return x
    
    @property
    def programming_function(self):
        if self.nr == self.mcu.define('MISO'):
            return 'MISO'
        if self.nr == self.mcu.define('MOSI'):
            return 'MOSI'
        if self.nr == self.mcu.define('SCK'):
            return 'SCK'
        if self.nr == self.mcu.define('SS'):
            return 'SS'

    @property
    def is_usb_plus(self):
        return self.nr == self.base.usb_plus_pin
            
    @property
    def is_usb_minus(self):
        return self.nr == self.base.usb_minus_pin
            
    def reset(self):
        return self.base.reset(self.nr)

    def write_pullup(self, value):
        return self.base.write_pullup(self.nr, value)
        
    # faster
    def read_digital(self):
        return self.base.read_digital(self.nr)
        
    def write_digital(self, value):
        return self.base.write_digital(self.nr, value)
    digital = property(read_digital, write_digital)
    
    # slower    
    def read_digital_in(self):
        return self.base.read_digital_in(self.nr)
    digital_in = property(read_digital_in)
        
    def read_digital_out(self):
        return self.base.read_digital_out(self.nr)
        
    def write_digital_out(self, value):
        return self.base.write_digital_out(self.nr, value)
    digital_out = property(read_digital_out, write_digital_out)

    def read_analog(self):
        return self.base.read_analog(self.nr)
    analog = property(read_analog)
    
    def read_analog_obj(self):
        return self.base.read_analog_obj(self.nr)
    analog_obj = property(read_analog_obj)
        
    def read_mode(self):
        return self.base.read_mode(self.nr)
        
    def write_mode(self, value):
        return self.base.write_mode(self.nr, value)
    mode = property(read_mode, write_mode)
        
        
class Pins(object):    
    def __init__(self, base, defines,mcu):
        self.base = base
        self.defines = defines
        self.mcu = mcu
        
    @property
    def range_all(self):
        return range(0, self.count)
    
    @property
    def range_digital(self):
        return range(0, self.defines.value('A0'))
    
    @property
    def range_analog(self):
        return range(self.defines.value('A0'), self.count)
        
    def write_pullup(self, pin_nr, value):
        value = bool(value)
        if self.read_mode(pin_nr) == INPUT:
            self.base.write_digital(pin_nr, value)
            
    def read_mode(self, pin_nr):
        bitmask = self.base.digitalPinToBitMask(pin_nr)
        port = self.base.digitalPinToPort(pin_nr)
        reg = self.base.portModeRegister(port);
        mode = OUTPUT if reg & bitmask else INPUT
        return mode
    
    def write_mode(self, pin_nr, x):
        assert pin_nr != self.usb_minus_pin
        assert pin_nr != self.usb_plus_pin
        if x == 'INPUT':
            x = INPUT
        if x == 'OUTPUT':
            x = OUTPUT
        self.base.write_mode(pin_nr, x)
        
    def read_digital(self, pin_nr):
        return self.base.read_digital(pin_nr)
    
    def write_digital(self, pin_nr, x):
        self.base.write_digital(pin_nr, x)
        
    def read_digital_out(self, pin_nr):
        if self.read_mode(pin_nr) == OUTPUT:
            return self.base.read_digital(pin_nr)
    
    def write_digital_out(self, pin_nr, x):
        self.base.write_mode(pin_nr, OUTPUT)
        self.base.write_digital(pin_nr, x)

    def read_digital_in(self, pin_nr):
        if self.read_mode(pin_nr) == INPUT:
            return self.base.read_digital(pin_nr)
    
    def read_analog(self, pin_nr):
        return self.base.read_analog(pin_nr)
    
    def read_analog_obj(self, pin_nr):
        return AnalogInputValue(self.mcu,pin_nr)

    
    @property
    @memoize()
    def count(self):
        '''
        HACK!
        '''  
        valid = [2 ** x for x in range(8)]
        for i in range(0, 100):
            x = self.base.digitalPinToBitMask(i)
            if x not in valid:
                assert i > 1
                return i
        assert 0
    
    @property
    @memoize()
    def count_digital(self):
        return len(self.range_digital)
    
    @property
    @memoize()
    def count_analog(self):
        return len(self.range_analog)
    
    def find(self, port, bit): 
        bitmask = 1 << bit
        for x in self.range_all:
            if bitmask == self.base.digitalPinToBitMask(x):
                if port == self.base.digitalPinToPort(x):
                    return x
                
    def reset(self, pin_nr):
        self.write_mode(pin_nr, INPUT)

    def reset_all(self):
        minus = self.usb_minus_pin
        plus = self.usb_plus_pin
        for x in self.range_all:
            if x != minus and x != plus:
                self.write_mode(x, INPUT)
                # turn off pullup
                self.write_digital(x, LOW)
                
    @property
    @memoize()
    def usb_minus_pin(self): 
        bit = self.defines.value('USB_CFG_DMINUS_BIT')
        port = self.defines.value('USB_CFG_IOPORT')
        return self.find(port, bit)
    
    @property
    @memoize()
    def usb_plus_pin(self): 
        bit = self.defines.value('USB_CFG_DPLUS_BIT')
        port = self.defines.value('USB_CFG_IOPORT')
        return self.find(port, bit)
    

class PinsLowLevel(object):
    def __init__(self, base):
        self.base = base
        
    def read_digital(self, pin_nr): 
        return self.base.usb_transfer(13, pin_nr)
    
    def write_digital(self, pin_nr, value): 
        self.base.usb_transfer(10, pin_nr, value)
    
    def read_analog(self, pin_nr):
        return self.base.usb_transfer(27, pin_nr)

    def write_mode(self, pin_nr, mode): 
        return self.base.usb_transfer(11, pin_nr, mode)
    
    @memoize()   
    def digitalPinToBitMask(self, pin):
        return self.base.usb_transfer(29, pin)
    
    @memoize()   
    def digitalPinToPort(self, pin):
        return self.base.usb_transfer(30, pin)
    
    @memoize()   
    def digitalPinToTimer(self, pin):
        return self.base.usb_transfer(36, pin)
    
    @memoize()   
    def analogInPinToBit(self, pin):
        return self.base.usb_transfer(37, pin)

    def portModeRegister(self, pin):
        return self.base.usb_transfer(31, pin)
    
    def portOutputRegister(self, pin):
        return self.base.usb_transfer(38, pin)
    
    def portInputRegister(self, pin):
        return self.base.usb_transfer(39, pin)
    
    def analogReference(self, value):
        self.usb_transfer(14, value)
        
class PinMixin(object):    
    
    @property
    @memoize()
    def lowlevel_pins(self):
        return PinsLowLevel(self.serializer)
#    
    @property
    @memoize()
    def pins(self):
        return Pins(self.lowlevel_pins, self.defines, self)
            
    @memoize()   
    def _pin(self, pin_nr):
        return Pin(self.pins, self, nr=pin_nr)

    def pin(self, pin_nr):
        return self._pin(pin_nr_as_int(pin_nr, self.define('A0')))
    
        
    
                
            
      

