Usage
===========

.. runblock:: pycon
    
    >>> from softusbduino import *
    >>>
    >>> # read defines
    >>> board = Arduino()
    >>> 
    >>> # reset pin directions
    >>> board.reset()
    >>>
    >>> # constants in python library
    >>> print '0x%X' % board.idVendor
    >>> print '0x%X' % board.idProduct
    >>> print board.bandgap_voltage
    >>>
    >>> # constants in firmware
    >>> print board.usbMinusPin
    >>> print board.usbPlusPin
    >>> print board.pinCount
    >>> print board.pinRange()
    >>> print board.pinRange('digital')
    >>> print board.pinRange('analog')
    >>>
    >>> # supply voltage
    >>> print board.vcc
    >>> print board.u_vcc
    >>>
    >>> # pin
    >>> print board.pin(8).nr
    >>> print board.pin('D8').nr
    >>> print board.pin('A2').nr
    >>> print board.pin('D13').programming_function
    >>>
    >>> # pin mode
    >>> board.pinMode(8, OUTPUT)
    >>> print board.readPinMode(8)
    >>> print board.pin('D8').mode
    >>> board.pin('D8').mode = INPUT
    >>> print board.readPinMode(8)
    >>> print board.pin('D8').mode
    >>>
    >>> # analog read
    >>> print board.pin('A2').analogRead()
    >>> print board.pin('A2').an_in
    >>> print board.pin('A2').u_an_in
    >>>
    >>> # digital read
    >>> print board.pin('D8').dig_in
    >>>
    >>> # pullup
    >>> pinD8 = board.pin('D8')
    >>> pinD8.pullup = True
    >>> print pinD8.pullup
    >>>
    >>> # digital write
    >>> board.pin('D8').dig_out = 1
    >>> print board.pin('D8').dig_out
    >>> board.pin('D8').dig_out = 0
    >>> print board.pin('D8').dig_out
    >>>
    >>> # PWM
    >>> print board.pin('D9').pwm_available
    >>> print board.pin('D9').timer_register_name
    >>> print board.pin('D9').pwm_frequencies_available
    >>> print board.pin('D9').pwm_frequency
    >>> print board.pin('D9').divisors_available
    >>> print board.pin('D9').divisor
    >>> board.pin('D9').divisor = 256
    >>> print board.pin('D9').pwm_frequency
    >>> print board.pin('D9').divisor
    >>> board.pin('D9').pwm_frequency = 38
    >>> print board.pin('D9').pwm_frequency
    >>> print board.pin('D9').divisor
    >>> board.pin('D9').pwm_out = 4
    >>>
    >>> # read defines
    >>> print board.defines.MCU_DEFINED
    >>> print board.defines.F_CPU
    >>> print board.defines.__DATE__
    >>> print board.defines.MOSI
    >>> print board.defines.USB_CFG_DMINUS_BIT
    >>> print board.defines.ARDUINO
    >>> print board.defines.__AVR_LIBC_VERSION__
    >>> print board.defines.A0
    >>>
    >>> # read/write register	
    >>> board.registers.DDRB = 0
    >>> print board.registers.DDRB
    >>> print board.pin(8).mode
    >>> board.registers.DDRB = 1
    >>> print board.registers.DDRB
    >>> print board.pin(8).mode
    >>> board.pin(8).mode = INPUT
    >>> print board.registers.DDRB
    >>> print board.pin(8).mode
    >>>
    >>>
    >>> board.reset()

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
 
