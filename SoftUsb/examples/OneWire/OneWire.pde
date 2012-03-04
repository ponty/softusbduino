// include before SoftUsb!
#include <OneWire.h>

#include <SoftUsb.h>

SoftUsb usb;

void setup()
{
	usb.begin();
}

void loop()
{
	usb.refresh();
}
