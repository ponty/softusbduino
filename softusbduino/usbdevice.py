from softusbduino.const import ID_VENDOR, ID_PRODUCT
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
#print 'REQUEST_TYPE_SEND',REQUEST_TYPE_SEND
#print 'REQUEST_TYPE_RECEIVE',REQUEST_TYPE_RECEIVE

#USBRQ_HID_GET_REPORT = 0x01
#USBRQ_HID_SET_REPORT = 0x09
#USB_HID_REPORT_TYPE_FEATURE = 0x03
#CUSTOM_RQ_SET_STATUS = 1
#CUSTOM_RQ_GET_STATUS = 2

#IDVENDOR, IDPRODUCT = 0x16c0, 0x05df

class ArduinoUsbDeviceError(Exception):
    pass


class ArduinoUsbDevice(object):
    """
    """
    
    def __init__(self, idVendor=ID_VENDOR, idProduct=ID_PRODUCT):
        """
        """
        self.idVendor = idVendor
        self.idProduct = idProduct

        self.device = usb.core.find(idVendor=self.idVendor,
                                    idProduct=self.idProduct)

        if not self.device:
            raise ArduinoUsbDeviceError("Device not found")

        self.firmware_test()
        
#    def write_bytes(self, data):
#        """
#        """
#        x = data + [0, 0, 0, 0]
#        self.device.ctrl_transfer(REQUEST_TYPE_SEND,
#                                 CUSTOM_RQ_SET_STATUS, # bRequest
#                                   x[0] + (x[1] << 8), # wValue
#                                   x[2] + (x[3] << 8), # wIndex
#                                 )
#    @traced
    def read_bytes(self, data):
        """
        """
        x = data + [0, 0, 0, 0,0]
        ls = self.device.ctrl_transfer(REQUEST_TYPE_RECEIVE,
                                 x[0], # bRequest
#                                 CUSTOM_RQ_GET_STATUS, # bRequest
                                   x[1] + (x[2] << 8), # wValue
                                   x[3] + (x[4] << 8), # wIndex
                                   20,
                                 )
        return list(ls)
    
        
    @property
    def productName(self):
        """
        """
        return getStringDescriptor(self.device, self.device.iProduct)

    
    @property
    def manufacturer(self):
        """
        """
        return getStringDescriptor(self.device, self.device.iManufacturer)


    
                                

