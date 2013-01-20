from dicts.sorteddict import SortedDict
from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
import inspect


def dump(obj):
    for attr in dir(obj):
        if not attr.startswith('__'):
            if not inspect.ismethod(getattr(obj, attr)):
# if not attr in 'vcc pins registers defines device register_ids'.split():
                    print "%-15s = %15s" % (attr, getattr(obj, attr))


@entrypoint
def usbdump():
    mcu = Arduino()

    print
    print '================================'
    print 'Arduino() attributes:'
    print '================================'
    dump(mcu)

    print
    print '================================'
    print 'Arduino().usb attributes:'
    print '================================'
    dump(mcu.usb)

    print
    print '================================'
    print 'Arduino().pins attributes:'
    print '================================'
    dump(mcu.pins)

    print
    print '================================'
    print 'Arduino().pin(nr) attributes:'
    print '================================'
    for nr in mcu.pins.range_all:
        print '---------- nr=%s ---------------' % nr
        dump(mcu.pin(nr))
        if mcu.pin(nr).pwm.available:
            print '--- pwm ---'
            dump(mcu.pin(nr).pwm)

    print
    print '================================'
    print 'Arduino().vcc attributes:'
    print '================================'
    dump(mcu.vcc)

    print
    print '================================'
    print 'Arduino().defines attributes:'
    print '================================'

    dump(mcu.defines)

    print
    print '================================'
    print 'Arduino().registers attributes:'
    print '================================'
    dump(mcu.registers)

    print

    print
    print '================================'
    print 'defines:'
    print '================================'
    for k, v in SortedDict(mcu.defines.as_dict()).items():
        print '%-20s = %18s' % (k, v)

    print
    print '================================'
    print 'registers:'
    print '================================'
    # , key=lambda x:mcu.registers.address(x[0]) # sort by address
    for k, v in SortedDict(mcu.registers.as_dict()).items():
        print '%-20s = 0x%02X @0x%2X (%s)' % (k, v, mcu.registers.address(k), mcu.registers.size(k))
