from eeml import Celsius
from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
from softusbduino.usbdevice import ArduinoUsbDeviceError
import eeml
import time

@entrypoint
def main(
        feed,
        stream,
        key,
         pin='D8',
         sleep=5,
         timeout=0,
         ):
    print 'pin:', pin
    print 'sleep:', sleep
    print 'timeout:', timeout
    print 'pachube:'
    print '  feed:', feed
    print '  stream:', stream
    print '  key:', key
    pa = eeml.Pachube(feed, key)

    def init():
        mcu = Arduino()
        mcu.pins.ground_unused([pin])
        bus = mcu.onewire.bus(pin)
        devs = bus.search()
        d = devs[0]
        print 'address=', d.address_str
        print 'address_valid=', d.address_valid
        print 'chip=', d.chip
        print 'resolution=', d.resolution, 'bit'
        mcu.watchdog.start(8)
        return mcu, d

    mcu, d = init()
    start = time.time()
    errors = 0

    def measure():
        x = d.scratchpad()
        print x.celsius, 'C', time.ctime(x.t), x.data, 'errors:', errors
        pa.update([
                   eeml.Data(stream, x.celsius, unit=Celsius()),
                   ])
        pa.put()

    while 1:
        try:
            measure()
        except ArduinoUsbDeviceError, e:
            print e
            errors += 1
            time.sleep(10)
            mcu, d = init()
            measure()

        time.sleep(sleep)
        if timeout > 0:
            if timeout < time.time() - start:
                break

