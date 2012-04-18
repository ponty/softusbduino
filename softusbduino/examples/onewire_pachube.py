from eeml import Celsius
from softusbduino.arduino import Arduino
from softusbduino.usbdevice import ArduinoUsbDeviceError
import eeml
import time


def main(
        feed,
        key,
        streams={},
         pins=[],
         sleep=5,
         sleep_after_error=60,
         timeout=0,
         ):
    print '----  config -----'
    print 'pins:', pins
    print 'sleep:', sleep
    print 'timeout:', timeout
    print 'pachube:'
    print '  feed:', feed
    print '  streams:', streams
    print '  key:', key
    pa = eeml.Pachube(feed, key)

    def init():
        print '----  init -----'
        mcu = Arduino()
#        mcu.watchdog.start(8)
#        mcu.pins.ground_unused([pin])
        alldevs = dict()
        for p in pins:
            print 'searching on pin:', p
            bus = mcu.onewire.bus(p)
            devs = bus.search()
            for d in devs:
                print 'device found:'
                print '  address=', d.address_str
                print '  address_valid=', d.address_valid
                print '  chip=', d.chip
                print '  resolution=', d.resolution, 'bit'
                alldevs[d.address_str] = d
        return alldevs

    alldevs = init()
    start = time.time()
    errors = 0

    def measure():
       print '----  measure -----'
       for stream, address in streams.items():
            d = alldevs.get(address, None)
            if d:
                x = d.scratchpad()
                print x.celsius, 'C',stream,address, time.ctime(x.t), x.data, 'errors:', errors
                pa.update([
                           eeml.Data(stream, x.celsius, unit=Celsius()),
                           ])
                try:
                    pa.put()
                except Exception, e:
                    print e

    restart = False
    while 1:
        try:
            if restart:
                alldevs = init()
                restart = False
            measure()
        except ArduinoUsbDeviceError, e:
            print e
            errors += 1
            restart = 1
            time.sleep(sleep_after_error)

        time.sleep(sleep)
        if timeout > 0:
            if timeout < time.time() - start:
                break

