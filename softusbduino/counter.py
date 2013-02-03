from __future__ import division
from memo import memoized
from uncertainties import ufloat
import logging
import time

log = logging.getLogger(__name__)


class CounterError(Exception):
    pass


class LowLevelCounter(object):
    def __init__(self, base):
        self.base = base

    def start_interrupt(self, gate_time_ms, startTCCR2B, usb_disconnect=False):
        return self.base.usb_transfer(90, int(usb_disconnect), startTCCR2B, word1=gate_time_ms)
    def read_count(self):
        return self.base.usb_transfer(91)

TOV1=0
WGM21=1
OCF2A=1
CS20=0
CS21=1
CS22=2

class Counter(object):
    def __init__(self, base, defines, mcu):
        self.base = base
        self.defines = defines
        self.mcu = mcu
        
    def   counter_init(self):
        reg=self.mcu.registers.proxy
        self.saveTCCR1A = reg.TCCR1A;
        self.saveTCCR1B = reg.TCCR1B;
        reg.TCCR1B = 0;
        reg.TCCR1A = 0;
        reg.TCNT1 = 0;
        reg.TIFR1 = (1 << TOV1);
        reg.TIMSK1 = 0;
        
    def timer_init(self):
        reg=self.mcu.registers.proxy

        self.saveTCCR2A = reg.TCCR2A;
        self.saveTCCR2B = reg.TCCR2B;
        reg.TCCR2B = 0;
        reg.TCCR2A = (1 << WGM21);


        reg.OCR2A = 124                 # div 125
        self.startTCCR2B = (1<<CS22) | (1<<CS20)   # div 128
        
        reg.TIFR2 = (1 << OCF2A);
        reg.TCNT2 = 0;


        
    def end(self):
        self.timer_shutdown();
        self.counter_shutdown();
    
    def   timer_shutdown(self):
        reg=self.mcu.registers.proxy
        reg.TCCR2B = 0;
        reg.TIMSK2 = 0;
        reg.TCCR2A = self.saveTCCR2A;
        reg.TCCR2B = self.saveTCCR2B;
    
    def   counter_shutdown(self):
        reg=self.mcu.registers.proxy
        reg.TCCR1B = 0;
        reg.TCCR1A = self.saveTCCR1A;
        reg.TCCR1B = self.saveTCCR1B;
    
    def run(self, gate_time_asked):
        self.gate_time_asked = gate_time_asked
        usb_disconnect=False
        reg=self.mcu.registers.proxy
        
        F_CPU = self.mcu.define('F_CPU')
        self.gate_freq=F_CPU/125/128
        x = int(gate_time_asked*self.gate_freq)
        self.gate_time = x/self.gate_freq
        
        self.counter_init()
        self.timer_init()
        self.base.start_interrupt(x, self.startTCCR2B, usb_disconnect=usb_disconnect)
        time.sleep(self.gate_time+0.1)
        
        if usb_disconnect:
            self.mcu.usb.disconnect()
            time.sleep(2)
            self.mcu.usb.connect()
        
        n=self.base.read_count()
        n=ufloat((n, 1))        
        self.frequency = n/self.gate_time
        return self.frequency

class CounterMixin(object):

    @property
    @memoized
    def counter(self):
        return Counter(self.lowlevel_counter, self.defines, self)

    @property
    @memoized
    def lowlevel_counter(self):
        return LowLevelCounter(self.serializer)
