from memo import memoized
from softusbduino.const import *
import logging
import time

log = logging.getLogger(__name__)

WDTO_15MS = 0
WDTO_30MS = 1
WDTO_60MS = 2
WDTO_120MS = 3
WDTO_250MS = 4
WDTO_500MS = 5
WDTO_1S = 6
WDTO_2S = 7
WDTO_4S = 8
WDTO_8S = 9

WDIE = 6
WDE = 3

class WatchdogError(Exception):
    pass


class LowLevelWatchdog(object):
    def __init__(self, base):
        self.base = base

    def reset(self):
        return self.base.usb_transfer(81)

    def enable(self, value):
        return self.base.usb_transfer(82, value)

    def reconnect(self):
        return self.base.usb_transfer(80)

    def disable(self):
        return self.base.usb_transfer(83)

    def write_auto_reset(self, value):
        return self.base.usb_transfer(84, value)

class Watchdog(object):
    values = {
                0.015: WDTO_15MS,
                0.030: WDTO_30MS,
                0.060: WDTO_60MS,
                0.120: WDTO_120MS,
                0.250: WDTO_250MS,
                0.500: WDTO_500MS,
                1: WDTO_1S,
                2: WDTO_2S,
                4: WDTO_4S,
                8: WDTO_8S,
                }

    def __init__(self, base, defines, mcu):
        self.base = base
        self.defines = defines
        self.mcu = mcu

    def reset(self):
        return self.base.reset()

    @property
    @memoized
    def WDTCSR(self):
        return self.mcu.register('WDTCSR')

    def start(self, sec):
        self.base.enable(self.values[sec])
        self.base.write_auto_reset(False)

    def stop(self):
        self.base.enable(self.values[1])
        self.base.write_auto_reset(True)

#    def write_timeout(self, sec):
##        self.WDTCSR.value |= (1 << WDE)
#        return self.base.enable(self.values[sec])

#    def disable(self):
##        self.WDTCSR.value &= ~(1 << WDIE)
##        self.WDTCSR.value &= ~(1 << WDE)
#       self.base.disable()

    def reconnect(self):
        self.base.reconnect()
        time.sleep(2)

#    def write_auto_reset(self, value):
#        self.base.write_auto_reset(value)

class WatchdogMixin(object):

    @property
    @memoized
    def watchdog(self):
        return Watchdog(self.lowlevel_watchdog, self.defines, self)


    @property
    @memoized
    def lowlevel_watchdog(self):
        return LowLevelWatchdog(self.serializer)




