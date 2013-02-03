from softusbduino.arduino import Arduino

dev = None


def setup():
    global dev
    dev = Arduino()
    dev.pins.reset()


def teardown():
    global dev
    dev.hardreset()


def test():
    dev.delay_test(0.0001, 'usbPoll', disable_interrupts=False)
    dev.delay_test(0.0001, 'usbFunctionSetup', disable_interrupts=False)
