from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino


@entrypoint
def main():
    mcu = Arduino()
    print 'Vcc=', mcu.vcc.voltage
