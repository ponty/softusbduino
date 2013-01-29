from memo import memoized
import logging
import time

log = logging.getLogger(__name__)


class DelayTestLowLevel(object):
    def __init__(self, base):
        self.base = base

    def delay_in_usbFunctionSetup(self, wait, flags):
        return self.base.usb_transfer(210, flags, word1=wait)

    def delay_in_usbPoll(self, wait, flags):
        return self.base.usb_transfer(211, flags, word1=wait)


class DelayTestMixin(object):

    @property
    @memoized
    def lowlevel_delaytest(self):
        return DelayTestLowLevel(self.serializer)

    def delay_test(self, wait, func, disable_interrupts=False, loop=True):
        '''

        :param wait: float (sec)  rounded to ms if > 1ms
        :param enable_interrupts: bool
        :param func: 'usbFunctionSetup' or 'usbPoll'
        '''
        func = func.lower()
        if func == 'usbPoll'.lower():
            f = self.lowlevel_delaytest.delay_in_usbPoll
            postsleep = 1.5 * wait
        elif func == 'usbFunctionSetup'.lower():
            f = self.lowlevel_delaytest.delay_in_usbFunctionSetup
            postsleep = 0
        else:
            assert 0

        flags = 0
        if disable_interrupts:
            flags += 1
        if loop:
            flags += 4

        ms = int(wait * 1000)
        if ms < 1:
            us = int(1000000 * wait)
            value = us
        else:
            value = ms
            flags += 2
        t1 = time.time()
        index = f(wait=value, flags=flags)
        t2 = time.time()
        dt = t2 - t1
        log.debug('delay_test took: %s ms   index=%s' % (round((dt)
                  * 1000, 2), index))
        if postsleep:
            log.debug('sleeping %s sec' % (postsleep))
            time.sleep(postsleep)
        return t2 - t1
