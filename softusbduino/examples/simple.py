from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino


@entrypoint
def main():
    mcu = Arduino()
    print 'F_CPU=', mcu.define('F_CPU')
    print 'DDRC=', mcu.register('DDRC').read_value()
