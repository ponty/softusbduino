from softusbduino.arduino import Arduino


def test1():
    dev = Arduino()
    dev.pins.reset()

# not working any more
#def test2():
#    dev = Arduino()
#    dev.hardreset()
