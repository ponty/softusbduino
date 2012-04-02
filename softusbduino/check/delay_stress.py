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
            interrupts=0,
            sleep_between_calls=0.1,
            wait=0.001,
         ):
    mcu = Arduino(auto_reconnect=False)

#    TEMPL = 'count={count:>5} fail={fail:>5} wait={wait:>5} ms in {func} int={interrupts} sleep={sleep_between_calls} s'
    count = 0
    fail = 0
    skip = int(2 / sleep_between_calls + 0.5)
    while 1:
        count += 1
        try:
            if count % skip == 0:
                print dict(
                               wait=1000 * wait,
                               func=func,
                               interrupts=interrupts,
                               sleep_between_calls=sleep_between_calls,
                               count=count,
                               fail=fail,
                               )
    
            mcu.delay_test(wait,
                             func,
                             interrupts=interrupts)
            time.sleep(sleep_between_calls)
            mcu.firmware_test()
            
        except (usb.USBError, ArduinoUsbDeviceError) , e:
            print('USBError: %s reconnect_time: %s s' % (str(e), reconnect_time))
            
            # time for reconnect
            time.sleep(reconnect_time)
            
            mcu.connect()
            fail += 1


