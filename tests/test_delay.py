from softusbduino.arduino import Arduino

dev = None


def setup():
    global dev
    dev = Arduino()
    dev.reset()


def teardown():
    global dev
    dev.reset()


def test():
    dev.delay_test(0.0001, 'usbPoll', interrupts=False)
    dev.delay_test(0.0001, 'usbFunctionSetup', interrupts=False)
