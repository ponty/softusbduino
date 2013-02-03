from memo import memoized
from softusbduino.const import *
from softusbduino.counter import CounterMixin
from softusbduino.defines import DefineMixin
from softusbduino.delaytest import DelayTestMixin
from softusbduino.onewire import OneWireMixin
from softusbduino.pin import PinMixin
from softusbduino.pwmpin import PwmMixin
from softusbduino.registers import RegisterMixin
from softusbduino.ser import SerializerMixin
from softusbduino.usbdevice import UsbDevice, UsbMixin
from softusbduino.vcc import VccMixin
from softusbduino.wd import WatchdogMixin
import logging
import time
import version

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
    WatchdogMixin,
    CounterMixin,
):
    Rout = 23
    analog_range = (0, 1023)
    bandgap_voltage = 1.1  # Volt
    adc_accuracy = 1

    def __init__(self,
                 #                 reset=True,
                 ground_usb_neihbours=True,
                 #                 vcc=None,
                 Rout=None,
                 **kwargs):
#        self.firmware_test()
#        if reset:
#            self.reset()
#        if ground_usb_neihbours:
#            self.ground_usb_neihbours()
#        if vcc:
#            self.vcc.voltage=vcc
        if Rout:
            self.Rout = Rout

    def firmware_test(self):
        assert self.define('MAGIC_NUMBER') == MAGIC_NUMBER

    def version_test(self):
        assert self.defines.SOFTUSBDUINO_FIRMWARE_VERSION == version.SOFTUSBDUINO_FIRMWARE_VERSION

    def hardreset(self):
        '''hard reset with watchdog
        slow
        '''
        t = self.watchdog.values[0]
        self.watchdog.start(t)
        self.usb.disconnect()
        time.sleep(t + 1)
        self.usb.connect()

    def ground_usb_neihbours(self):
        self.pins.ground_usb_neihbours()

    @property
    @memoized
    def model(self):
        return self.define('MCU_DEFINED').strip('_').split('_')[-1]
