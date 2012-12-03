from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
from softusbduino.usbdevice import ArduinoUsbDeviceError
import logging
import time
import usb

log = logging


def check_delay(
    mcu,
    func,
    interrupts,
    sleep_between_calls,
    reconnect_time,
):

    def test_range(step):
        log.debug('step= %s ms' % step)
        wait = None
        try:
            for i in range(2, 11):
                wait = i * step / 1000.0
                log.debug('testing %s s' % wait)
                mcu.delay_test(wait,
                               func,
                               interrupts=interrupts)
                time.sleep(sleep_between_calls)
                mcu.firmware_test()
        except (usb.USBError, ArduinoUsbDeviceError), e:
            log.debug('USBError: %s reconnect_time: %s s' % (
                str(e), reconnect_time))
            # time for reconnect
            time.sleep(reconnect_time)

            mcu.usb.connect()

            # min reached
            if wait <= 0.000002:
                raise

            return wait - step / 1000.0

    step = 1
    max_good = test_range(step)
    if max_good is None:
        step = 10
    else:
        step = 0.001

    while 1:
        max_good = test_range(step)
#            print 5555, max_good
        if max_good is None:
            step *= 10
        else:
            break
        if step > 100:
            break
    return max_good


def print_delay(count, **kw):
    mindelay = min([check_delay(**kw) for _ in range(count)])
    TEMPL = 'max {delay:>5} ms in {func} int={interrupts} sleep={sleep_between_calls} count={count}'
    print TEMPL.format(delay=1000 * mindelay, count=count, **kw)


@entrypoint
def main(
):
    mcu = Arduino(auto_reconnect=False)

    kw = dict(
        mcu=mcu,
        reconnect_time=1,
        func='usbFunctionSetup',
        interrupts=False,
        sleep_between_calls=0.1,
        count=10,
    )

    def run(**kw):
        print_delay(**kw)

    kw['func'] = 'usbFunctionSetup'

    run(**kw)

#    print '=============='

    kw['func'] = 'usbPoll'

    run(**kw)

#    print '=============='

    kw['func'] = 'usbFunctionSetup'
    kw['interrupts'] = True

    run(**kw)

#    print '=============='

    kw['func'] = 'usbPoll'

    run(**kw)
