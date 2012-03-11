#!/usr/bin/env python
from bunch import Bunch
from entrypoint2 import entrypoint
from softusbduino.const import ID_VENDOR, ID_PRODUCT
import fcntl
import logging
import usb
logging.basicConfig(level=logging.DEBUG)

USBDEVFS_RESET = 21780

def find():
    print("searching for device (%x:%x)" % (ID_VENDOR, ID_PRODUCT))
#    dev = usb.core.find(id_vendor=ID_VENDOR,
#                        id_product=ID_PRODUCT,
#                        )
    dev=None
    for b in usb.busses():
        for x in b.devices:
            if x.idVendor == ID_VENDOR and x.idProduct == ID_PRODUCT:
                dev = Bunch()
                dev.bus=b.dirname
                dev.address=x.devnum
                break
    if not dev:
        print("device not found")
    return dev

def usbstr(i):
    s=str(i)
    s='000'[0:3-len(s)]+s
    return s

def usbfs_filename(dev):
    return '/dev/bus/usb/%s/%s' % (usbstr(dev.bus), usbstr(dev.address))

def reset1(dev):
    fname=usbfs_filename(dev)
    print("Resetting USB device %s" % fname)
    with open(fname, 'w') as fd:
        rc = fcntl.ioctl (fd, USBDEVFS_RESET, 0)
        if (rc < 0):
            print("Error in ioctl")
    print("OK")
    
def reset2(dev):
    dev.reset() # not working

@entrypoint
def main():    
    dev=find()
    if dev:
        reset1(dev)    


