from eeml import Celsius
from softusbduino.arduino import Arduino
from softusbduino.usbdevice import ArduinoUsbDeviceError
import eeml
import time
import logging
#from threading import Thread
from softusbduino.onewire import OneWireError

log = logging.getLogger(__name__)

mcu = Arduino()


def fsleep(s, mcu):
    s=int(s)
    log.debug('sleep %s sec' % s)
    time.sleep(s)

def fsleep2(s, mcu):
    s=int(s)
    log.debug('sleep %s sec' % s)
    if mcu:
        #log.debug('watchdog reset 1')
        mcu.watchdog.reset()
    for x in range(s):
        time.sleep(1)
        if mcu:
            #log.debug('watchdog reset 2')
            mcu.watchdog.reset()


def main(
        feed,
        key,
        streams={},
         pins=[],
         sleep=5,
         sleep_after_error=30,
         #timeout=0,
         repeat=None,
         watchdog=0,
         ):
    #Arduino().usb.reset()
    log.debug('----  config -----')
    log.debug('pins:%s', pins)
    log.debug('sleep:%s', sleep)
    #log.debug('timeout:%s', timeout)
    log.debug('pachube:')
    log.debug('  feed:%s', feed)
    log.debug('  streams:%s', streams)
    log.debug('  key:%s', key)
    pa = eeml.Pachube(feed, key)

    def init():
        log.debug('----  init -----')
#        if watchdog:
#            mcu.watchdog.start(watchdog)
#        mcu.pins.ground_unused([pin])
        alldevs = dict()
        for p in pins:
         try:
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
         except OneWireError, e:
           log.debug('OneWireError',e)
            
        return alldevs

    alldevs = init()
    #mcu = Arduino()
    #while 1:
        #mcu.usb.connect()
    #    bus = mcu.onewire.bus('A0')
    #    devs = bus.search()
    #    print devs
    #    d=devs[0]
    #    x = d.scratchpad()
    #    print x.celsius
        #del mcu
        #print 555
        #assert 0
    #    time.sleep(1)
    #mcu.usb.disconnect()

    #start = time.time()
    errors = [0,0]
    def measure():
        log.debug('----  measure -----')
        for stream, address in streams.items():
            d = alldevs.get(address, None)
            if d:
              try:
                x = d.scratchpad()
                log.debug('%s C %s %s %s errors:%s' % (x.celsius, stream, address, x.data, errors))
                pa.update([
                           eeml.Data(stream, round(x.celsius, 2), unit=Celsius()),
                           ])
              except OneWireError, e:
                log.debug(e)
                print stream, e
                pa.update([
                           eeml.Data(stream, None, unit=Celsius()),
                           ])
        def put():
            log.debug('put')
            try:
                pa.put()
            except Exception, e:
                log.debug(e)
                errors[1] += 1
#                raise
        put()
#        t = Thread(target=put)
#        t.start()
    restart = False
    i=0
    while 1:
        try:
#            if restart:
#                log.debug('restart')
#                mcu, alldevs = init()
#                restart = False
            measure()
        except OneWireError, e:
            log.debug(e)
#            errors[0] += 1
#            restart = 1
#            fsleep(sleep_after_error)
#            log.debug('usb reset')
#            Arduino().usb.reset()
            fsleep(sleep_after_error, mcu=None)
        i+=1
        if repeat and repeat <= i:
            break

        fsleep(sleep, mcu=mcu)
        #if timeout > 0:
        #    if timeout < time.time() - start:
        #        break

