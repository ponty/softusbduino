from decorator import decorator
from memo import memoized
from softusbduino.const import ID_VENDOR, ID_PRODUCT
import fcntl
import logging
import time
import usb

log = logging.getLogger(__name__)

DESC_TYPE_STRING = 0x03
ENDPOINT_IN = 0x80
CTRL_TYPE_VENDOR = (2 << 5)
CTRL_RECIPIENT_DEVICE = 0
CTRL_IN = 0x80
REQ_GET_DESCRIPTOR = 6


REQUEST_TYPE_RECEIVE = CTRL_IN | CTRL_TYPE_VENDOR | CTRL_RECIPIENT_DEVICE


class ArduinoUsbDeviceError(Exception):
    pass


@decorator
def reconnect_if_dropped(f, self, *args, **kw):
    """
    """
    connect = False
    retry = 3
    wait = 2
    while 1:
        try:
#            if connect:
#                log.debug("reconnect  retries: %s" % (retry))
#                self.connect()
            return f(self, *args, **kw)
        except (usb.USBError, ArduinoUsbDeviceError), e:
            log.debug("USBError: %s" % (e))
            self.disconnect()
            raise ArduinoUsbDeviceError(str(e))

#            if self.auto_reconnect:
#                if retry <= 0:
#                    raise
#                connect = True
#                retry -= 1
#                time.sleep(wait)
#            else:
#                raise


class UsbDevice(object):
    """
    """

    def __init__(self, id_vendor=ID_VENDOR, id_product=ID_PRODUCT, auto_reconnect=True):
        """
        """
        self.id_vendor = id_vendor
        self.id_product = id_product
        self.auto_reconnect = auto_reconnect

        self.connect()

    device = None
    device_handle = None

    def search(self):
        log.debug(
            "searching for device %x:%x" % (self.id_vendor, self.id_product))
        for b in usb.busses():
            for d in b.devices:
                if d.idVendor == self.id_vendor and d.idProduct == self.id_product:
                    # all info is empty with PyUSB 1.x (bug?)
                    log.debug("found device  bus:%s dev:%s" %
                              (b.dirname, d.filename))
                    return b, d

    def connect(self):
        log.debug("connect")
        ls = self.search()
        if not ls:
            raise ArduinoUsbDeviceError("Device (%x:%x) not found" %
                                        (self.id_vendor, self.id_product))
        self.bus, self.device = ls
        if self.device:
            self.device_handle = self.device.open()
#        for b in usb.busses():
#            for x in b.devices:
#                if x.idVendor == self.id_vendor and x.idProduct == self.id_product:
#                    self.device = x
#                    self.device_handle = self.device.open()
#                    break

#        self.device = usb.core.find(idVendor=self.id_vendor,
#                                    idProduct=self.id_product)
    def disconnect(self):
        log.debug("disconnect")
        if self.device_handle:
            del self.device_handle
            self.device_handle = None
        if self.device:
            del self.device
            self.device = None
        if self.bus:
            del self.bus
            self.bus = None

    def getStringDescriptor(self, index):
        """
        """

    #    response = device.ctrl_transfer(
    #                                    bmRequestType=usb.util.ENDPOINT_IN,
    #                                    bRequest=usb.legacy.REQ_GET_DESCRIPTOR,
    #                                    wValue=(usb.util.DESC_TYPE_STRING << 8) | index,
    #                                    wIndex=0, # language id
    #                                    data_or_wLength=255
    #                                    ) # length

        response = self.device_handle.controlMsg(
            requestType=ENDPOINT_IN,
            request=REQ_GET_DESCRIPTOR,
            value=(DESC_TYPE_STRING << 8) | index,
            index=0,  # language id
            buffer=255
            #                                   timeout=1000,
        )

        # TODO: Refer to 'libusb_get_string_descriptor_ascii' for error
        # handling

        return str(''.join(map(chr, response[2:])))
        #.decode('utf-16')

    #@reconnect_if_dropped
    def usb_transfer_bytes(self, data):
        """
        """
        if not self.device:
            self.connect()
        x = data + [0, 0, 0, 0, 0]
        ls = self.device_handle.controlMsg(
            requestType=REQUEST_TYPE_RECEIVE,
            request=int(x[0]),  # bRequest
            value=int(x[1]) + (int(x[2]) << 8),
            index=int(x[3]) + (int(x[4]) << 8),
            buffer=20,
            timeout=1000,
        )

#        ls = self.device.ctrl_transfer(REQUEST_TYPE_RECEIVE,
#                                 x[0], # bRequest
##                                 CUSTOM_RQ_GET_STATUS, # bRequest
#                                   x[1] + (x[2] << 8), # wValue
#                                   x[3] + (x[4] << 8), # wIndex
#                                   20,
##                                   timeout=1000,
#                                 )
        return list(ls)

    @property
    def productName(self):
        """
        """
        if not self.device:
            self.connect()
        return self.getStringDescriptor(self.device.iProduct)

    @property
    def manufacturer(self):
        if not self.device:
            self.connect()
        return self.getStringDescriptor(self.device.iManufacturer)

    def reset(self, backend='libusb'):
        if backend == 'libusb':
            self.reset_libusb()
        elif backend == 'usbfs':
            self.reset_usbfs()
        else:
            raise ValueError('Unknown backend: %s' % backend)

    def reset_libusb(self):
        if not self.device:
            self.connect()
        self.device_handle.reset()
        self.disconnect()

    def reset_usbfs(self):
        'only as root'
        if not self.device:
            self.connect()

        def usbstr(i):
            s = str(i)
            s = '000'[0:3 - len(s)] + s
            return s

        def usbfs_filename(root):
            address = self.device.filename
            bus = self.bus.dirname
            return '/%s/bus/usb/%s/%s' % (root, usbstr(bus), usbstr(address))

        USBDEVFS_RESET = 21780
        try:
            fd = open(usbfs_filename('dev'), 'w')
        except IOError:
            fd = open(usbfs_filename('proc'), 'w')

        rc = fcntl.ioctl(fd, USBDEVFS_RESET, 0)
        if (rc < 0):
            log.debug("Error in ioctl rc=" % rc)

        self.disconnect()


class UsbMixin(object):

    @property
    @memoized
    def usb(self):
        return UsbDevice()
