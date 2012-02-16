softusbduino is a Python package and Arduino firmware library. 
They can be used together to control the Arduino board over USB in Python.
Possible usage: prototyping or creating simple low speed USB devices.

Links:
 * home: https://github.com/ponty/softusbduino
 * documentation: http://ponty.github.com/softusbduino

Hierarchy:
 Python Application -> softusbduino python library -> PyUSB_ -> libusb_ -> 
 USB cable -> V-USB_ hardware -> Arduino_ -> V-USB_ library -> softusbduino firmware

Features:
 - Possible usage: prototyping or creating simple low speed USB devices.
 - firmware should be load only once to the Arduino board.
 - 1 low level call takes 2 ms in tests
 - python library functions:
	 - read or write all registers
	 - call arduino functions
	 - read many defines (example: F_CPU)
 - Python USB back end: PyUSB_ 1.0 library
 - Arduino USB back end: V-USB_ library
  
Known problems:
 - tested only on Linux + arduino 0022 + ATmega88 board
 - pull-up read is not implemented
 - PWM read is not implemented
 - PWM config is hardcoded
 
similar projects:
 - https://github.com/HashNuke/Python-Arduino-Prototyping-API
 - http://code.google.com/p/vusb-for-arduino/

Basic usage of prototyping
==============================
::
	
	from softusbduino.protoapi import *
	
	def setup():
	    pinMode(13, OUTPUT);   
	      
	def loop():
	    digitalWrite(13, HIGH);   
	    delay(1000);              
	    digitalWrite(13, LOW);    
	    delay(1000);              
	
	sketch = Sketch(setup, loop)
	sketch.run()


Installation
=======================

General
----------

 * install Python_
 * install pip_
 * install arduino_
 * install SoftUsb subdirectory as arduino library
     - Manual installation: http://arduino.cc/en/Guide/Environment#libraries
     - Automatic installation:  
        - install confduino_
        - install the library: ``python -m confduino.libinstall https://github.com/ponty/softusbduino/zipball/master``
 * install python package::

    # as root
    pip install https://github.com/ponty/softusbduino/zipball/master    
 
Ubuntu
----------
::

    sudo apt-get install arduino python-pip
    sudo pip install confduino
    sudo pip install https://github.com/ponty/softusbduino/zipball/master
    sudo python -m confduino.libinstall https://github.com/ponty/softusbduino/zipball/master
    # optional for examples
    sudo pip install matplotlib traits traitsui

Upload firmware
----------------
::

  1. start Arduino
  2. open examples > SoftUsb > Simple
  3. upload to board 


.. _arduino: http://arduino.cc/
.. _python: http://www.python.org/
.. _confduino: https://github.com/ponty/confduino
.. _libusb: http://www.libusb.org/
.. _PyUSB: http://pyusb.sourceforge.net/
.. _V-USB: http://vusb.wikidot.com/
.. _pip: http://pip.openplans.org/
