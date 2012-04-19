from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino


@entrypoint
def main():
    mcu = Arduino()
    print 'reset'

    #mcu.usb.reset()
    mcu.usb.reset_libusb()
    #mcu.usb.reset_usbfs()
