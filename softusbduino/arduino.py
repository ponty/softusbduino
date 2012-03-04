from remember.memoize import memoize
from softusbduino import version
from softusbduino.const import *
from softusbduino.defines import DefineMixin
from softusbduino.delaytest import DelayTestMixin
from softusbduino.onewire import OneWireMixin
from softusbduino.pin import PinMixin
from softusbduino.pwmpin import PwmMixin
from softusbduino.registers import RegisterMixin
from softusbduino.ser import SerializerMixin
from softusbduino.usbdevice import UsbDevice, UsbMixin
from softusbduino.vcc import VccMixin
import logging

log = logging.getLogger(__name__)

class ArduinoUsbError(Exception):
    pass

class Arduino(
              UsbMixin, 
              SerializerMixin,
              RegisterMixin, 
              OneWireMixin, 
              VccMixin, 
              DefineMixin,
              DelayTestMixin,
              PinMixin,
              PwmMixin,
              ):
    Rout = 15    
    analog_range = (0, 1023)
    bandgap_voltage = 1.1 # Volt
    adc_accuracy = 2
    
    def __init__(self, reset=True, **kwargs):
        self.firmware_test()
        if reset:
            self.reset()
      
    def firmware_test(self):
        assert self.define('MAGIC_NUMBER') == MAGIC_NUMBER
    
    def version_test(self):
        assert self.defines.SOFTUSBDUINO_FIRMWARE_VERSION == version.SOFTUSBDUINO_FIRMWARE_VERSION

    def reset(self):
        self.pins.reset_all()       
    
    

