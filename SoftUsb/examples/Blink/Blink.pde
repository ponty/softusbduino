// include before SoftUsb!
//#include <OneWire.h>

#include <SoftUsb.h>

SoftUsb usb;

void setup()
{
	usb.begin();
}
const int led1 = 12;
const int led2 = 13;

byte x1=0;
uint32_t i1=0;

byte x2=0;
uint32_t i2=0;

void loop()
{
	pinMode(led1, OUTPUT);
	digitalWrite(led1, x1);
	i1++;
	if(i1>50000)
	{
		i1=0;
		x1=!x1;
	}
	
	pinMode(led2, OUTPUT);
	digitalWrite(led2, x2);
	i2++;
	if(i2>5000)
	{
		i2=0;
		x2=!x2;
	}
	
	usb.refresh();
}

