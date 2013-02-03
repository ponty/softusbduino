from nose.tools import eq_
from softusbduino.arduino import Arduino, OUTPUT, INPUT
from softusbduino.protoapi import *
from test_pin import ok_an

dev = None


def test():
    eq_(A0, 14)
    eq_(A1, 15)
    ok_an(analogRead(0))

    pinMode(9, OUTPUT)
    analogWrite(9, 45)
    pinMode(10, OUTPUT)
    digitalWrite(10, HIGH)
    digitalRead(11)
