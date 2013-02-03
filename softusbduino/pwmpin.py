from __future__ import division
from memo import memoized
from softusbduino.const import OUTPUT
import logging

log = logging.getLogger(__name__)

base_divisor = {
    3: 512,
    5: 256,
    6: 256,
    9: 512,
    10: 512,
    11: 512,
}


class BiDict():
    def __init__(self, dic):
        self.norm = dic
        self.inv = dict([(v, k) for k, v in dic.items()])

_div1 = BiDict({
               1: 1,
               2: 8,
               3: 64,
               4: 256,
               5: 1024,
               })
_div2 = BiDict({
               1: 1,
               2: 8,
               3: 32,
               4: 64,
               5: 128,
               6: 256,
               7: 1024,
               })
divisor_mapping = {
    3: _div2,
    5: _div1,
    6: _div1,
    9: _div1,
    10: _div1,
    11: _div2,
}
# timer_register = {
#                3:'TCCR2B',
#                5:'TCCR0B',
#                6:'TCCR0B',
#                9:'TCCR1B',
#                10:'TCCR1B',
#                11:'TCCR2',
#                }

# TIMERS = ['NOT_ON_TIMER',
#          'TCCR0B',
#          'TCCR0B',
#          'TCCR1B',
#          'TCCR1B',
#          'TCCR2',
#          'TCCR2B',
#          'TCCR2B',
#          # TODO:
#          #        'TIMER3A',
#          #        'TIMER3B',
#          #        'TIMER3C',
#          #        'TIMER4A',
#          #        'TIMER4B',
#          #        'TIMER4C',
#          #        'TIMER5A',
#          #        'TIMER5B',
#          #        'TIMER5C',
#          ]

TIMERS_A = ['NOT_ON_TIMER',
            'TCCR0A',
            'TCCR0A',
            'TCCR1A',
            'TCCR1A',
            None,  # TODO: atmega8
            'TCCR2A',
            'TCCR2A',
            ]

TIMERS_B = ['NOT_ON_TIMER',
            'TCCR0B',
            'TCCR0B',
            'TCCR1B',
            'TCCR1B',
            'TCCR2',
            'TCCR2B',
            'TCCR2B',
            ]

timer_mask = 7  # 0b111

# TODO: pwm_mode  read/write
# TODO: read mappings


class PwmPin(object):
    def __init__(self, pin):
        self.pin = pin
        self.base = pin.mcu.pwm

    @property
    def available(self):
        return self.base.available(self.pin.nr)

    def write_value(self, value):
        return self.base.write_value(self.pin.nr, value)

    @property
    def divisors_available(self):
        return self.base.divisors_available(self.pin.nr)

    def read_divisor(self):
        return self.base.read_divisor(self.pin.nr)

    def write_divisor(self, value):
        return self.base.write_divisor(self.pin.nr, value)
    divisor = property(read_divisor, write_divisor)

    @property
    def timer_register_name(self):
        return self.base.timer_register_name(self.pin.nr)

    @property
    def timer_register_name_a(self):
        return self.base.timer_register_name(self.pin.nr, variant='A')

    @property
    def timer_register_name_b(self):
        return self.base.timer_register_name(self.pin.nr, variant='B')

    def read_timer_mode(self):
        return self.base.read_timer_mode(self.timer_register_name_b)

    def write_timer_mode(self):
        return self.base.write_timer_mode(self.timer_register_name_b)
    timer_mode = property(read_timer_mode, write_timer_mode)

    @property
    def base_divisor(self):
        return self.base.base_divisor(self.pin.nr)

    @property
    def frequencies_available(self):
        return self.base.frequencies_available(self.pin.nr)

    def read_frequency(self):
        return self.base.read_frequency(self.pin.nr)

    def write_frequency(self, f):
        return self.base.write_frequency(self.pin.nr, f)
    frequency = property(read_frequency, write_frequency)

    def read_wgm(self):
        return self.base.read_wgm(self.pin.nr)
    wgm = property(read_wgm, None)

    def set_high_freq_around_pwm(self, top, fill):
        return self.base.set_high_freq_around_pwm(self.pin.nr, top, fill)

    def set_high_freq_around(self, freq):
        return self.base.set_high_freq_around(self.pin.nr, freq)


class PwmError(Exception):
    pass


class Pwm(object):
    def __init__(self, mcu, base):
        self.base = base
        self.mcu = mcu
        self.registers = mcu.registers
        self.F_CPU = mcu.define('F_CPU')

    def available(self, pin_nr):
        timer_id = self._timer_id(pin_nr)
        return timer_id > 0 and timer_id < len(TIMERS_B)
#        return pin_nr in timer_register

    def _check(self, pin_nr):
        if not self.available(pin_nr):
            raise PwmError('pwm not available for pin: %s' % pin_nr)

    def write_value(self, pin_nr, value):
        self._check(pin_nr)
        assert self.mcu.pins.read_mode(pin_nr) == OUTPUT
        self.base.write_pwm(pin_nr, value)

    def divisors_available(self, pin_nr):
        try:
            return divisor_mapping[pin_nr].norm.values()
        except KeyError:
            return []

    def read_divisor(self, pin_nr):
        self._check(pin_nr)
        d = divisor_mapping[pin_nr]
        reg_name = self.timer_register_name(pin_nr)
        return d.norm[self.read_timer_mode(reg_name)]

    def write_divisor(self, pin_nr, value):
        self._check(pin_nr)
        d = divisor_mapping[pin_nr]
        reg_name = self.timer_register_name(pin_nr)
        self.write_timer_mode(reg_name, d.inv[value])

#    def write_wgm(self, pin_nr, value):
#        ''' Waveform generation mode'''
#        self._check(pin_nr)
#        reg_name = self.timer_register_name(pin_nr)
#        self.write_timer_mode(reg_name, d.inv[value])

    def _timer_id(self, pin_nr):
        return self.mcu.lowlevel_pins.digitalPinToTimer(pin_nr)

    def timer_register_name(self, pin_nr, variant='B'):
        self._check(pin_nr)
        i = self._timer_id(pin_nr)
        return dict(A=TIMERS_A, B=TIMERS_B)[variant][i]

    def read_timer_mode(self, reg_name):
        return self.registers.read_value(reg_name) & timer_mask

    def write_timer_mode(self, reg_name, value):
        assert value <= 7
        old = self.registers.read_value(reg_name) & ~timer_mask
        self.registers.write_value(reg_name, old | value)

    def base_divisor(self, pin_nr):
        self._check(pin_nr)
        return base_divisor[pin_nr]

    def calculate_frequency(self, pin_nr, divisor):
        return 1.0 * self.F_CPU / self.base_divisor(pin_nr) / divisor

    def frequencies_available(self, pin_nr):
        ls = [self.calculate_frequency(
            pin_nr, x) for x in self.divisors_available(pin_nr)]
        ls.sort()
        return ls

    def read_frequency(self, pin_nr):
        self._check(pin_nr)
        wgm = self.read_wgm(pin_nr)
        if wgm == 14:
            # high freq mode
            return self.F_CPU / self.registers.read_value('ICR1')
        else:
            return self.calculate_frequency(pin_nr, self.read_divisor(pin_nr))

    def write_frequency(self, pin_nr, value):
        self._check(pin_nr)
        d = divisor_mapping[pin_nr]
        for x in self.divisors_available(pin_nr):
            f = self.calculate_frequency(pin_nr, x)
            if abs(f - value) <= 1:
                reg_name = self.timer_register_name(pin_nr)
                self.write_timer_mode(reg_name, d.inv[x])
                return

    def read_wgm(self, pin_nr):
        self._check(pin_nr)
        rega = self.timer_register_name(pin_nr, variant='A')
        regb = self.timer_register_name(pin_nr)
        if regb == 'TCCR1B':
            maskb = 0b00011000
        else:
            maskb = 0b00001000
        maska = 0b00000011
        a = self.registers.read_value(rega) & maska
        b = self.registers.read_value(regb) & maskb
        return a + (b >> 1)

    def _check_high_freq(self, pin_nr):
        if pin_nr not in [9, 10]:
            raise PwmError('high freq pwm not available for pin: %s' % pin_nr)

    def set_high_freq_around_pwm(self, pin_nr, top, fill):
        'F_CPU/divisor'
        d = top
        self._check_high_freq(pin_nr)
        assert d >= 2

        self.write_divisor(pin_nr, 1)
        self.write_value(pin_nr, 128)
#        self.registers.write_value('TCNT1', 0)
#        self.registers.write_value('ICR1', d)
#        self.registers.write_value('OCR1A', fill)
#        self.registers.write_value('OCR1B', fill)

        reg = self.registers.proxy
        reg.TCCR1A = 0b00000010 + (0b11110000 & reg.TCCR1A)
        reg.TCCR1B = 0b00011001

        reg.TCNT1 = 0
        reg.ICR1 = d
        reg.OCR1A = fill
        reg.OCR1B = fill

    def set_high_freq_around(self, pin_nr, freq):
        top = int(self.F_CPU / freq + 0.5)
        assert 1 < top < (1 << 16)
        self.set_high_freq_around_pwm(pin_nr, top, int(top / 2))


class PwmLowLevel(object):
    def __init__(self, base):
        self.base = base

    def write_pwm(self, pin_nr, value):
        self.base.usb_transfer(12, pin_nr, value)


class PwmPinMixin(object):
    @property
    @memoized
    def pwm(self):
        return PwmPin(self)


class PwmMixin(object):
    @property
    @memoized
    def lowlevel_pwm(self):
        return PwmLowLevel(self.serializer)

    @property
    @memoized
    def pwm(self):
        return Pwm(self, self.lowlevel_pwm)
