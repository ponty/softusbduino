from eeml import Celsius
from softusbduino.arduino import Arduino
from softusbduino.usbdevice import ArduinoUsbDeviceError
import eeml
import time
import logging

log = logging.getLogger(__name__)


def fsleep(s, mcu):
    log.debug('sleep %s sec' % s)
    if mcu:
        mcu.watchdog.reset()
    for x in range(int(s)):
        time.sleep(1)
        if mcu:
            mcu.watchdog.reset()


def main(
        feed,
        key,
        streams={},
         pins=[],
         sleep=5,
         sleep_after_error=300,
         timeout=0,
         ):
    Arduino().usb.reset()
    log.debug('----  config -----')
    log.debug('pins:%s', pins)
    log.debug('sleep:%s', sleep)
    log.debug('timeout:%s', timeout)
    log.debug('pachube:')
    log.debug('  feed:%s', feed)
    log.debug('  streams:%s', streams)
    log.debug('  key:%s', key)
    pa = eeml.Pachube(feed, key)

    def init():
        log.debug('----  init -----')
        mcu = Arduino()
        mcu.watchdog.start(2)
#        mcu.pins.ground_unused([pin])
        alldevs = dict()
        for p in pins:
            log.debug('searching on pin:%s', p)
            bus = mcu.onewire.bus(p)
            devs = bus.search()
            for d in devs:
                log.debug('device found:')
                log.debug('  address=%s', d.address_str)
                log.debug('  address_valid=%s', d.address_valid)
                log.debug('  chip%s', d.chip)
                log.debug('  resolution=%s bit', d.resolution)
                alldevs[d.address_str] = d
        return mcu, alldevs

    mcu, alldevs = init()
    start = time.time()
    errors = [0,0]

    def measure():
        log.debug('----  measure -----')
        for stream, address in streams.items():
            d = alldevs.get(address, None)
            if d:
                x = d.scratchpad()
                log.debug('%s C %s %s %s errors:%s' % (x.celsius, stream, address, x.data, errors))
                pa.update([
                           eeml.Data(stream, round(x.celsius, 1), unit=Celsius()),
                           ])
        log.debug('put')
        try:
            pa.put()
        except Exception, e:
            log.debug(e)
            errors[1] += 1
            raise ArduinoUsbDeviceError(str(e))

    restart = False
    while 1:
        try:
            if restart:
                log.debug('restart')
                mcu, alldevs = init()
                restart = False
            measure()
            fsleep(sleep, mcu=mcu)
        except Exception, e:
            log.debug(e)
            errors[0] += 1
            restart = 1
#            fsleep(sleep_after_error)
#            log.debug('usb reset')
#            Arduino().usb.reset()
            fsleep(sleep_after_error, mcu=None)

        if timeout > 0:
            if timeout < time.time() - start:
                break

