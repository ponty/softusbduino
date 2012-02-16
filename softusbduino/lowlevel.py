from softusbduino.comm import CommunicationMixin
from softusbduino.const import *
from usbdevice import ArduinoUsbDevice
import logging
from remember.memoize import memoize

log = logging.getLogger(__name__)


class ArduinoLowLevel(ArduinoUsbDevice, CommunicationMixin):
    def analogRead(self, pin):
        x = self.read_any(27, pin)
        return x

    def analogWrite(self, pin, value):
        self.read_any(12, pin, value)
        
    def analogReference(self, value):
        self.read_any(14, value)
        
    def digitalWrite(self, pin, value): 
        self.read_any(10, pin, value)
    
    def digitalRead(self, pin): 
        return self.read_any(13, pin)
    
    def pinMode(self, pin, mode): 
        '''
        Configures the specified pin to behave either as an input or an output. 
        
        http://www.arduino.cc/en/Reference/pinMode
        
        :param pin: the number of the pin whose mode you wish to set
        :param mode: either INPUT or OUTPUT 
        '''   
        return self.read_any(11, pin, mode)
    
    @memoize()   
    def digitalPinToBitMask(self, pin):
        return self.read_any(29, pin)
    @memoize()   
    def digitalPinToPort(self, pin):
        return self.read_any(30, pin)
    @memoize()   
    def digitalPinToTimer(self, pin):
        return self.read_any(36, pin)
    @memoize()   
    def analogInPinToBit(self, pin):
        return self.read_any(37, pin)

    def portModeRegister(self, pin):
        return self.read_any(31, pin)
    def portOutputRegister(self, pin):
        return self.read_any(38, pin)
    def portInputRegister(self, pin):
        return self.read_any(39, pin)
    

    @memoize()   
    def read_int_define(self, reg_id):
        return self.read_any(51, reg_id)
    
    @memoize()   
    def read_special_define(self, reg_id):
        return self.read_any(reg_id)
