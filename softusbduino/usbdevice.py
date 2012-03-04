from decorator import decorator
from remember.memoize import memoize
from softusbduino.const import ID_VENDOR, ID_PRODUCT
import time
import usb # 1.0 not 0.4


def getStringDescriptor(device, index):
    """
    """
    response = device.ctrl_transfer(usb.util.ENDPOINT_IN,
                                    usb.legacy.REQ_GET_DESCRIPTOR,
                                    (usb.util.DESC_TYPE_STRING << 8) | index,
                                    0, # language id
                                    255) # length

    # TODO: Refer to 'libusb_get_string_descriptor_ascii' for error handling
    
    return response[2:].tostring().decode('utf-16')


REQUEST_TYPE_SEND = usb.util.build_request_type(usb.util.CTRL_OUT,
                                                usb.util.CTRL_TYPE_VENDOR,
                                                usb.util.CTRL_RECIPIENT_DEVICE)

REQUEST_TYPE_RECEIVE = usb.util.build_request_type(usb.util.CTRL_IN,
                                                usb.util.CTRL_TYPE_VENDOR,
                                                usb.util.CTRL_RECIPIENT_DEVICE)


class ArduinoUsbDeviceError(Exception):
    pass


@decorator
def reconnect_if_dropped(f, self, *args, **kw):
    """
    """
    connect = False
    retry = 3
    while 1:
        try:
            if connect:
                self.usb_connect()
            return f(self, *args, **kw)
        except usb.USBError or ArduinoUsbDeviceError:
            if self.auto_reconnect:
                if retry <= 0:
                    raise
                connect = True
                retry -= 1
                time.sleep(1)
            else:
                raise
        
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

    def connect(self):
        self.device = usb.core.find(idVendor=self.id_vendor,
                                    idProduct=self.id_product)

        if not self.device:
            raise ArduinoUsbDeviceError("Device not found")
            
    @reconnect_if_dropped
    def usb_transfer_bytes(self, data):
        """
        """
        if not self.device:
            self.connect()
        x = data + [0, 0, 0, 0, 0]
        ls = self.device.ctrl_transfer(REQUEST_TYPE_RECEIVE,
                                 x[0], # bRequest
#                                 CUSTOM_RQ_GET_STATUS, # bRequest
                                   x[1] + (x[2] << 8), # wValue
                                   x[3] + (x[4] << 8), # wIndex
                                   20,
#                                   timeout=1000,
                                 )
        return list(ls)
    
        
    @property
    def productName(self):
        """
        """
        if not self.device:
            self.connect()
        return getStringDescriptor(self.device, self.device.iProduct)

    
    @property
    def manufacturer(self):
        """
        """
        if not self.device:
            self.connect()
        return getStringDescriptor(self.device, self.device.iManufacturer)


class UsbMixin(object):    
    
    @property
    @memoize()
    def usb(self):
        return UsbDevice()
    
    
                                

