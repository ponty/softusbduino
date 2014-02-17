from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
import time
from softusbduino.onewire import OneWireError


def search(mcu, pins):
    alldevs = dict()
    for p in pins:
        try:
            print('searching on pin:%s'% p)
            bus = mcu.onewire.bus(p)
            devs = bus.search()
            for d in devs:
                print('device found:')
                print('  address=%s'% d.address_str)
                print('  address_valid=%s'% d.address_valid)
                print('  chip=%s'% d.chip)
                print('  resolution=%s bit'% d.resolution)
                alldevs[d.address_str] = d
        except OneWireError, e:
            print('OneWireError', e)

    return alldevs

@entrypoint
def main(
    pins='A0,A1,A2,D5,D6,D7',
    timeout=10,
):
    pins=pins.split(',')
    mcu = Arduino()
    print '--> search'
    devs = search(mcu, pins).values()

    print '--> read'
    start = time.time()
    while 1:
        for d in devs:
            x = d.scratchpad()
            print x.celsius, 'C', '[%s]' % d.address_str, time.ctime(x.t), x.data
            time.sleep(0.1)
            if timeout > 0:
                if timeout < time.time() - start:
                    break
