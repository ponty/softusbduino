from softusbduino.protoapi import *

dev = None


def test():
    analogRead(0)

    pinMode(9, OUTPUT)
    analogWrite(9, 45)
    pinMode(10, OUTPUT)
    digitalWrite(10, HIGH)
    digitalRead(11)
