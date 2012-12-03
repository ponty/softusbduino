from memo import memoized


class DelayTestLowLevel(object):
    def __init__(self, base):
        self.base = base

    def delay_in_usbFunctionSetup(self, wait, interrupts, milli):
        return self.base.usb_transfer(210, interrupts, milli, word=wait)

    def delay_in_usbPoll(self, wait, interrupts, milli):
        return self.base.usb_transfer(211, interrupts, milli, word=wait)


class DelayTestMixin(object):

    @property
    @memoized
    def lowlevel_delaytest(self):
        return DelayTestLowLevel(self.serializer)

    def delay_test(self, wait, func, interrupts=False):
        '''

        :param wait: float (sec)  rounded to ms if > 1ms
        :param enable_interrupts: bool
        :param func: 'usbFunctionSetup' or 'usbPoll'
        '''
        func = func.lower()
        if func == 'usbPoll'.lower():
            f = self.lowlevel_delaytest.delay_in_usbPoll
        elif func == 'usbFunctionSetup'.lower():
            f = self.lowlevel_delaytest.delay_in_usbFunctionSetup
        else:
            assert 0
        interrupts = bool(interrupts)
        ms = int(wait * 1000)
        if ms < 1:
            us = int(1000000 * wait)
            value = us
            milli = 0
        else:
            value = ms
            milli = 1
        f(wait=value, interrupts=interrupts, milli=milli)
