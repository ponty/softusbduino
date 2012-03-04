Usage
===========

.. runblock:: pycon
    
    >>> from softusbduino import *
    >>>
    >>> mcu = Arduino()
    >>> 
    >>> # reset pin directions
    >>> mcu.reset()
    >>>
    >>> # constants in python library
    >>> print '0x%X' % mcu.usb.id_vendor
    >>> print '0x%X' % mcu.usb.id_product
    >>> print mcu.bandgap_voltage
    >>>
    >>> # constants in firmware
    >>> print mcu.pins.usb_minus_pin
    >>> print mcu.pins.usb_plus_pin
    >>> print mcu.pins.count
    >>> print mcu.pins.count_digital
    >>> print mcu.pins.count_analog
    >>> print mcu.pins.range_all
    >>> print mcu.pins.range_digital
    >>> print mcu.pins.range_analog
    >>>
    >>> # supply voltage
    >>> print mcu.vcc.voltage
    >>> print mcu.vcc.u_voltage
    >>>
    >>> # pin
    >>> print mcu.pin(8).nr
    >>> print mcu.pin('D8').nr
    >>> print mcu.pin('A2').nr
    >>> print mcu.pin('D13').programming_function
    >>>
    >>> # pin mode
    >>> mcu.pins.write_mode(8, OUTPUT)
    >>> print mcu.pins.read_mode(8)
    >>> print mcu.pin('D8').read_mode()
    >>> print mcu.pin('D8').mode
    >>> mcu.pin('D8').mode = INPUT
    >>> print mcu.pins.read_mode(8)
    >>>
    >>> # analog read
    >>> print mcu.pins.read_analog(15)
    >>> print mcu.pin('A2').read_analog()
    >>> print mcu.pin('A2').analog
    >>>
    >>> # digital read
    >>> print mcu.pins.read_digital(8)
    >>> print mcu.pin('D8').read_digital()
    >>> print mcu.pin('D8').digital
    >>>
    >>> # pullup
    >>> mcu.pins.write_pullup(8, HIGH)
    >>> mcu.pin('D8').write_pullup(HIGH)
    >>>
    >>> # digital write
    >>> mcu.pins.write_mode(8, OUTPUT)
    >>> mcu.pins.write_digital(8, HIGH)
    >>> mcu.pin('D8').write_digital(HIGH)
    >>> mcu.pin('D8').digital = HIGH
    >>>
    >>> # PWM
    >>> print mcu.pin('D9').pwm.available
    >>> print mcu.pin('D9').pwm.timer_register_name
    >>> print mcu.pin('D9').pwm.frequencies_available
    >>> print mcu.pin('D9').pwm.frequency
    >>> print mcu.pin('D9').pwm.divisors_available
    >>> print mcu.pin('D9').pwm.divisor
    >>> mcu.pin('D9').pwm.divisor = 256
    >>> print mcu.pin('D9').pwm.frequency
    >>> print mcu.pin('D9').pwm.divisor
    >>> mcu.pin('D9').pwm.frequency = 38
    >>> print mcu.pin('D9').pwm.frequency
    >>> print mcu.pin('D9').pwm.divisor
    >>> mcu.pins.pwm.write_value(9, 54)
    >>> mcu.pin('D9').pwm.write_value(44)
    >>> mcu.pin('D9').pwm.value = 34
    >>>
    >>> # read defines
    >>> print mcu.define('F_CPU')
    >>> print mcu.defines.value('F_CPU')
    >>> print mcu.defines.exists('F_CPU')
    >>>
    >>> print mcu.define('MCU_DEFINED')
    >>> print mcu.define('F_CPU')
    >>> print mcu.define('__DATE__')
    >>> print mcu.define('MOSI')
    >>> print mcu.define('USB_CFG_DMINUS_BIT')
    >>> print mcu.define('ARDUINO')
    >>> print mcu.define('__AVR_LIBC_VERSION__')
    >>> print mcu.define('A0')
    >>>
    >>> # read/write register	
    >>> mcu.register('DDRB').value = 0
    >>> print mcu.registers.read_value('DDRB')
    >>> print mcu.register('DDRB').read_value()
    >>> print mcu.register('DDRB').value
    >>> print mcu.pin(8).mode
    >>> mcu.register('DDRB').value = 1
    >>> print mcu.register('DDRB').value
    >>> print mcu.pin(8).mode
    >>> mcu.pin(8).mode = INPUT
    >>> print mcu.register('DDRB').value
    >>> print mcu.pin(8).mode
    >>>
    >>>
    >>> mcu.reset()

Code generation
-----------------

Integer defines should be listed in softusbduino/intdefs.csv.
String defines are hardcoded.
Registers and MCU names are read from `AVR Libc`_ directory (/usr/lib/avr/include/avr/).

Run codegen.py to update generated files:
 - softusbduino/generated_registers.csv
 - SoftUsb/generated_registers.h
 - SoftUsb/generated_intdefs.h
 - SoftUsb/generated_mcu.h
 - SoftUsb/generated_version.h


.. _`AVR Libc`: http://www.nongnu.org/avr-libc/
 
