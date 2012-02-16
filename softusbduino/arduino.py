'''
http://code.google.com/p/pyduino/
https://github.com/HashNuke/Python-Arduino-Prototyping-API
'''
from nose.tools import eq_
from softusbduino.const import *
from softusbduino.defines import Defines
from softusbduino.lowlevel import ArduinoLowLevel
from softusbduino.pin import Pin
from softusbduino.registers import RegisterMixin, Registers
from uncertainties import ufloat
import logging
import time

log = logging.getLogger(__name__)

#def filter_analog(fread, nr):
#    '''
#    median filter
#    '''
#    values = [fread() for _ in range(nr)]
#    values.sort()
#    return values[int(nr / 2)]    

class ArduinoUsbError(Exception):
    pass

class Arduino(ArduinoLowLevel, RegisterMixin):
    Rout = 15    
#    filter_size = None
    analog_range = (0,1023)

    def __init__(self, reset=True, **kwargs):
        self.defines = Defines(self)
        self.registers = Registers(self)
        ArduinoLowLevel.__init__(self, **kwargs)
        if reset:
            self.reset()

#    def analogRead(self, pin):
#        if self.filter_size and self.filter_size > 1:
#            return filter_analog(lambda :ArduinoLowLevel.analogRead(self, pin), self.filter_size)
#        else:
#            return ArduinoLowLevel.analogRead(self, pin)
        
    def firmware_test(self):
        eq_( self.defines.MAGIC_NUMBER , MAGIC_NUMBER)

    def pin(self, pin_nr):
        return Pin(self, nr=pin_nr)
    
    def pinAnalog(self, pin_nr):
        return Pin(self, nr='A%s' % pin_nr)
    
    def reset(self):
        minus = self.usbMinusPin
        plus = self.usbPlusPin
        for x in self.pinRange():
            if x != minus and x != plus:
                self.pinMode(x, INPUT)
                # turn off pullup
                self.digitalWrite(x, LOW)
            
    def pinRange(self, kind='all'):
        if kind == 'all':
            return range(0, self.pinCount)
        if kind == 'digital':
            return range(0, self.defines.A0)
        if kind == 'analog':
            return range(self.defines.A0, self.pinCount)
        assert 0
        
    def readPinMode(self, pin): 
        '''inverse of pinMode()'''
        bitmask = self.digitalPinToBitMask(pin)
        port = self.digitalPinToPort(pin)
        reg = self.portModeRegister(port);
        mode = OUTPUT if reg & bitmask else INPUT
        return mode
    
    def findPin(self, port, bit): 
        bitmask = 1 << bit
        for x in self.pinRange():
            if bitmask == self.digitalPinToBitMask(x):
                if port == self.digitalPinToPort(x):
                    return x
                
    @property
    def pinCount(self):
        '''
        HACK!
        '''  
        valid = [2 ** x for x in range(8)]
        for i in range(0, 100):
            x = self.digitalPinToBitMask(i)
            if x not in valid:
                assert i > 1
                return i
        assert 0
            
      
    @property
    def usbMinusPin(self): 
        bit = self.defines.USB_CFG_DMINUS_BIT
        port = self.defines.USB_CFG_IOPORT
        return self.findPin(port, bit)
    
    @property
    def usbPlusPin(self): 
        bit = self.defines.USB_CFG_DPLUS_BIT
        port = self.defines.USB_CFG_IOPORT
        return self.findPin(port, bit)
    
    
    bandgap_voltage = 1.1 # Volt
    
    @property
    def  vcc(self):
        return self.u_vcc.nominal_value
    
    adc_accuracy = 2
    @property
    def  u_vcc(self):
        '''
        Vcc with uncertainty
        '''
        self.registers.ADMUX = 0b01001110
        time.sleep(0.002) # Wait for Vref to settle
        self.registers.ADCSRA |= 0b01000000
        while self.registers.ADCSRA & 0b01000000:
            time.sleep(0.001)
        result = self.registers.ADCL;
        result |= self.registers.ADCH << 8;
        error = self.adc_accuracy
        result = (self.bandgap_voltage * 1024L) / ufloat((result, error));
    
        return result
    
            

