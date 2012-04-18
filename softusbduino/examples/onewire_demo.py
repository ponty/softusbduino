from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
import time


@entrypoint
def main(
         pin='D8',
         timeout=10,
         ):
    mcu = Arduino()
    bus = mcu.onewire.bus(pin)
    print '--> search'
    devs = bus.search()
    for d in devs:
        print 'device found:'
        print '  address=', d.address_str
        print '  address_valid=', d.address_valid
        print '  chip=', d.chip
        print '  resolution=', d.resolution, 'bit'

    print '--> read'
    start = time.time()
    while 1:
        for d in devs:
            x = d.scratchpad()
            print x.celsius, 'C', '[%s]'%d.address_str, time.ctime(x.t), x.data
            time.sleep(0.1)
            if timeout > 0:
                if timeout < time.time() - start:
                    break
