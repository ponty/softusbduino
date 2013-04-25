from entrypoint2 import entrypoint
from softusbduino.version import __version__
import platform

try:
    import usb
    HAS_USB = True
except ImportError:
    HAS_USB = False

try:
    import usb.legacy
    HAS_USB_10 = True
except ImportError:
    HAS_USB_10 = False


@entrypoint
def main():
    ''' print versions
    '''

    if HAS_USB:
        if HAS_USB_10:
            pyusb = '1.x'
        else:
            pyusb = '0.x'
    else:
        pyusb = 'missing'

    print 'platform:', platform.platform()
    print 'python:', platform.python_version()
    print 'pyusb:', pyusb
    print 'softusbduino:', __version__
