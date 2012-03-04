'''
  Analog input, analog output, serial output
 
 Reads an analog input pin, maps the result to a range from 0 to 255
 and uses the result to set the pulsewidth modulation (PWM) of an output pin.
 Also prints the results to the serial monitor.
 
 The circuit:
 * potentiometer connected to analog pin 0.
   Center pin of the potentiometer goes to the analog pin.
   side pins of the potentiometer go to +5V and ground
 * LED connected from digital pin 9 to ground
 
  Converted from Arduino example.
'''

from softusbduino.protoapi import *

# These constants won't change.  They're used to give names
# to the pins used:
analogInPin = A0;  # Analog input pin that the potentiometer is attached to
analogOutPin = 9; # Analog output pin that the LED is attached to

sensorValue = 0;        # value read from the pot
outputValue = 0;        # value output to the PWM (analog out)

def setup():
    # initialize serial communications at 9600 bps:
    Serial_begin(9600); 


def loop():
    # read the analog in value:
    sensorValue = analogRead(analogInPin);            
    # map it to the range of the analog out:
    outputValue = map(sensorValue, 0, 1023, 0, 255);  
    # change the analog out value:
    analogWrite(analogOutPin, outputValue);           
    
    # print the results to the serial monitor:
    Serial_print("sensor = " );                       
    Serial_print(sensorValue);      
    Serial_print("\t output = ");      
    Serial_println(outputValue);   
    
    # wait 10 milliseconds before the next loop
    # for the analog-to-digital converter to settle
    # after the last reading:
    delay(10);                     

sketch = Sketch(setup, loop)
sketch.run()