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

