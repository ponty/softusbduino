from eeml import Celsius
from entrypoint2 import entrypoint
from softusbduino import Arduino
import eeml
import time


@entrypoint
def main(
        API_URL,
        API_KEY,
         pin='D8',
         sleep=10,
         timeout=0,
         ):
    print 'pin:', pin
    print 'sleep:', sleep
    print 'timeout:', timeout
    print 'API_KEY:', API_KEY
    print 'API_URL:', API_URL
    pa = eeml.Pachube(API_URL, API_KEY)
    mcu = Arduino()
    bus = mcu.onewire.bus(pin)
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
        pa.update([
                   eeml.Data('pince', x.celsius, unit=Celsius()),
                   ])
        pa.put()

        time.sleep(sleep)
        if timeout > 0:
            if timeout < time.time() - start:
                break
