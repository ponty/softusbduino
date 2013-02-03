from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino


@entrypoint
def main(backend='libusb'):
    mcu = Arduino()
    print 'reset using backend:' + backend
    mcu.usb.reset(backend=backend)
    # mcu.usb.reset_libusb()
    # mcu.usb.reset_usbfs()
