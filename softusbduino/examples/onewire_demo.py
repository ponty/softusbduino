from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
import time


@entrypoint
def main(
         pin='D9',
         timeout=10,
         ):
    mcu = Arduino()
    bus = mcu.bus1wire(pin)
    devs = bus.search()
    d = devs[0]
    print 'address=', d.address_str
    print 'address_valid=', d.address_valid
    print 'chip=', d.chip
    print 'resolution=', d.resolution, 'bit'
    
    start = time.time()
    while 1:
        x = d.scratchpad()
        print x.celsius, 'C', time.ctime(x.t), x.data
        time.sleep(0.1)
        if timeout > 0:
            if timeout < time.time() - start:
                break

