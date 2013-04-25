from __future__ import division
from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
from softusbduino.usbdevice import ArduinoUsbDeviceError
import logging
import time
import usb

log = logging


@entrypoint
def main(
    reconnect_time=5,
    func='usbPoll',
    disable_interrupts=0,
    sleep_between_calls=0,
    delay=0.001,
):
    mcu = Arduino()
    mcu.pins.reset()

    count = 0
    fail = 0
    t1 = time.time()
    while 1:
        count += 1
        t2 = time.time()
        if (t2 - t1) > 2:
            t1 = t2
            print dict(
                delay=delay,
                func=func,
                disable_interrupts=disable_interrupts,
                sleep_between_calls=sleep_between_calls,
                count=count,
                fail=fail,
            )
        try:
            mcu.delay_test(delay,
                           func,
                           disable_interrupts=disable_interrupts)
            time.sleep(sleep_between_calls)
            mcu.firmware_test()

        except (usb.USBError, ArduinoUsbDeviceError), e:
            print('USBError: %s reconnect_time: %s s' % (str(
                e), reconnect_time))

            # time for reconnect
            time.sleep(reconnect_time)

#            mcu.connect()
            fail += 1
