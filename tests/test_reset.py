from softusbduino.arduino import Arduino


def test1():
    dev = Arduino()
    dev.pins.reset()


def test2():
    dev = Arduino()
    dev.hardreset()
