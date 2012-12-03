from __future__ import division
from memo import memoized
from softusbduino.const import *
import logging
import time

log = logging.getLogger(__name__)


class CounterError(Exception):
    pass


class LowLevelCounter(object):
    def __init__(self, base):
        self.base = base

    def reset_variables(self):
        return self.base.usb_transfer(90)

    def write_period(self, value):
        return self.base.usb_transfer(91, word=value)

    def read_tics(self):
        return self.base.usb_transfer(92)

    def read_counter_overflows(self):
        return self.base.usb_transfer(93)

    def start_interrupt(self):
        return self.base.usb_transfer(94)

TOIE0 = 0
CS10 = 0
CS11 = 1
CS12 = 2
CS20 = 0
CS21 = 1
CS22 = 2
WGM20 = 0
WGM21 = 1
# WGM22=3
OCIE2A = 1
PSRASY = 1


class Counter(object):
    def __init__(self, base, defines, mcu):
        self.base = base
        self.defines = defines
        self.mcu = mcu

    def start(self, gate_time):
        F_CPU = self.mcu.define('F_CPU')
        TCCR1A = self.mcu.register('TCCR1A')
        TCCR1B = self.mcu.register('TCCR1B')
#        TCNT1 = self.mcu.register('TCNT1')
        TCNT1H = self.mcu.register('TCNT1H')
        TCNT1L = self.mcu.register('TCNT1L')
#        TCNT2 = self.mcu.register('TCNT2')
#        TIFR1 = self.mcu.register('TIFR1')
#        TIMSK0 = self.mcu.register('TIMSK0')
#        TIMSK1 = self.mcu.register('TIMSK1')
        TIMSK2 = self.mcu.register('TIMSK2')

        TCCR2A = self.mcu.register('TCCR2A')
        TCCR2B = self.mcu.register('TCCR2B')
        OCR2A = self.mcu.register('OCR2A')
        GTCCR = self.mcu.register('GTCCR')

#        TCNT2 = self.mcu.register('TCNT2')
        TCNT2 = self.mcu.register('TCNT2')

        # TIMSK0.value &= ~(1 << TOIE0)       # disable Timer0  #disable  millis and delay
        # time.sleep(1)      # wait if any ints are pending

#        if (f_comp == 0):
#             f_comp = 1  # 0 is not allowed in del us
        # hardware counter setup ( refer atmega168.pdf chapter 16-bit counter1)
        TCCR1A.value = 0                  # reset timer/counter1 control register A
        TCCR1B.value = 0                     # reset timer/counter1 control register A
        TCNT1H.value = TCNT1L.value = 0                      # counter value = 0

        prescaler = 128
        divider = 125

        self.base.reset_variables()
        period = int(F_CPU / prescaler / divider * gate_time)
        print 'period', period
        self.base.write_period(period)

        # set timer/counter1 hardware as counter , counts events on pin T1 ( arduino pin 5)
        # normal mode, wgm10 .. wgm13 = 0

#        TCCR1B.value |= (1 << CS10) # External clock source on T1 pin. Clock on rising edge.
#        TCCR1B.value |= (1 << CS11)
#        TCCR1B.value |= (1 << CS12)

        # timer2 setup / is used for frequency measurement gatetime generation
        TCCR2A.value = 0
        TCCR2B.value = 0

        # timer 2 presaler set to 128 / timer 2 clock = 16Mhz / 256 = 62500 Hz
        TCCR2B.value |= (1 << CS20)
        TCCR2B.value &= ~(1 << CS21)
        TCCR2B.value |= (1 << CS22)
#        prescaler = 128

        # set timer2 to CTC Mode with OCR2A is top counter value
        TCCR2A.value &= ~(1 << WGM20)
        TCCR2A.value |= (1 << WGM21)
        # TCCR2A &= ~(1 << WGM22) #???
        OCR2A.value = 124                # CTC divider by 125
#        divider=125

#        f_ready = 0                  # reset period measure flag
#        f_tics = 0                   # reset interrupt counter
        GTCCR.value = (1 << PSRASY)        # reset prescaler counting
        TCNT2.value = 0                    # timer2=0
#        TCNT1.value = 0                    # Counter1 = 0

                                    # External clock source on T1 pin. Clock on rising edge.
#        TCCR1B.value |= (1 << CS12) | (0 << CS11) | (1 << CS10)        #   start counting now
# TCCR1B.value |= (0 << CS12) | (0 << CS11) | (1 << CS10)        #   start
# counting now
        TCCR1B.value |= (1 << CS12) | (
            1 << CS11) | (1 << CS10)  # start counting now
#        time.sleep(2)
#        TIMSK2.value |= (1 << OCIE2A)       # enable Timer2 Interrupt
        self.base.start_interrupt()
        time.sleep(gate_time + 0.2)
        time.sleep(2)

        print 'tics:', self.base.read_tics(),
        print 'ovf:', self.base.read_counter_overflows(),
        print 'TCNT1', TCNT1L.value + (TCNT1H.value << 8),
        print 'TCNT1H', TCNT1H.value,
        print 'TCNT1L', TCNT1L.value
        n = TCNT1L.value + (TCNT1H.value << 8) + (
            self.base.read_counter_overflows() << 16)
        print 'n', n,
        t = 1 / F_CPU * prescaler * period * divider
        print 't', t,
        f = n / t
        print 'f', f

        xx = t * 20000000 / 256 / 256
        xx2 = 256 * (xx - int(xx))
#        print 'xx',int(xx),int(xx2)
        return f


class CounterMixin(object):

    @property
    @memoized
    def counter(self):
        return Counter(self.lowlevel_counter, self.defines, self)

    @property
    @memoized
    def lowlevel_counter(self):
        return LowLevelCounter(self.serializer)
