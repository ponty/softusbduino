from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino


@entrypoint
def main():
    mcu = Arduino()
    p = mcu.pin(9)
    print p.read_mode()
    p.write_mode(1)
    print p.read_mode()
    mcu.reset()
    print p.read_mode()
