from nose.tools import eq_
from softusbduino.codegen.avrlib import avr_define_value_list, avr_define_value


def test_defines():
    eq_([1, 3], avr_define_value_list(
        defines=['PINB1', 'PINB3'], mcu='__AVR_ATmega8__'))
    eq_([None, 7, 6, 5], avr_define_value_list(
        defines=['xxx', 'PIND7', 'PIND6', 'PIND5'], mcu='__AVR_ATmega88__'))
# eq_([None],  avr_define_value_list(defines=['UDR0'],
# mcu='__AVR_ATmega88__'))


def test_define():
    eq_(1, avr_define_value(define='PINB1', mcu='__AVR_ATmega8__'))
    eq_(7, avr_define_value(define='PINB7', mcu='__AVR_ATmega48__'))
    eq_(0, avr_define_value(define='PINC0', mcu='__AVR_ATmega88__'))
    eq_(None, avr_define_value(define='PINA1', mcu='__AVR_ATmega8__'))
#    eq_(None,  avr_define_value(define='UDR0', mcu='__AVR_ATmega88__'))
