'''
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  Converted from Arduino example.
'''

from softusbduino.protoapi import *


def setup():
    pinMode(13, OUTPUT)


def loop():
    digitalWrite(13, HIGH)
    delay(1000)
    digitalWrite(13, LOW)
    delay(1000)


sketch = Sketch(setup, loop)
sketch.run()
