from __future__ import division
from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
from softusbduino.usbdevice import ArduinoUsbDeviceError
import logging
import time
import usb

log = logging.getLogger(__name__)

'''
http://vusb.wikidot.com/troubleshooting

"6.- Interrupts and Timing
... Also make sure you're not disabling interrupts for longer
than a few milliseconds,
or that you have more than 10ms between calls to usbPoll() ..."



'''


def check_delay(
    mcu,
    func,
    disable_interrupts,
    sleep_between_calls,
    reconnect_time,
    loop,
):
    def test_range(step):
        log.debug('step= %d us' % (step))
        delay = None
        try:
            for i in range(2, 11):
                delay = i * step
                log.debug('testing %d us' % (delay))
                mcu.delay_test(delay / 1e6,
                               func,
                               disable_interrupts=disable_interrupts,
                               loop=loop,
                               )
                time.sleep(sleep_between_calls)
                mcu.firmware_test()
        except (usb.USBError, ArduinoUsbDeviceError), e:
            log.debug('USBError: %s reconnect_time: %s s' % (
                str(e), reconnect_time))
            # time for reconnect
            time.sleep(reconnect_time)

            mcu.usb.connect()

            # min reached
            if delay <= 2e-6:
                raise

            return delay - step

    step = 1 * 1000
    max_good = test_range(step)
    if max_good is None:
        step = 10 * 1000
    else:
        step = 1

    while 1:
        max_good = test_range(step)
        if max_good is None:
            step *= 10
        else:
            break
        if step >= 2 * 1e6:
            return step 
#             break
    return max_good

TEMPL_usbPoll = '''
void loop()
{
usbPoll();
%s
usbPoll();
}
'''.strip()

TEMPL_usbFunctionSetup = '''
usbMsgLen_t usbFunctionSetup(uchar data[8])
{
%s
}
'''.strip()

TEMPL_noInterrupts = '''
noInterrupts();
%s
interrupts();
'''.strip()


def pseudocode(func, disable_interrupts, **kw):
    s = 'delay(t);'

    if disable_interrupts:
        s = TEMPL_noInterrupts % s

    if func == 'usbFunctionSetup':
        s = TEMPL_usbFunctionSetup % s
    elif func == 'usbPoll':
        s = TEMPL_usbPoll % s
    return s
TEMPL = '''
--------------------------------------------------------
disable interrupts={disable_interrupts}
delay position in code={func}
number of measurements={count}
pseudocode:
{pseudocode}

max delays in us (sorted): {delay}
--------------------------------------------------------
'''.strip()


def print_delay(count, **kw):
    delayms_ls = [check_delay(**kw) for _ in range(count)]
    delayms_ls.sort()
#    mindelay = min(delay_ls)
    print TEMPL.format(delay=delayms_ls,
                       count=count,
                       pseudocode=pseudocode(**kw),
                       **kw)


@entrypoint
def main():
    mcu = Arduino()
    mcu.pins.reset()

    kw = dict(
        mcu=mcu,
        reconnect_time=1,
        disable_interrupts=False,
        sleep_between_calls=0,
        count=5,
        loop=1,
    )

    def run(**kw):
        print_delay(**kw)

    kw['disable_interrupts'] = False

    kw['func'] = 'usbFunctionSetup'
    run(**kw)

    kw['func'] = 'usbPoll'
    run(**kw)

    kw['disable_interrupts'] = True

    kw['func'] = 'usbFunctionSetup'
    run(**kw)

    kw['func'] = 'usbPoll'
    run(**kw)
