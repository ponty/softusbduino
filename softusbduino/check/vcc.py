from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino


@entrypoint
def main():
    mcu = Arduino()
    print 'mcu.bandgap_voltage =', mcu.bandgap_voltage
    print 'mcu.vcc.voltage =', mcu.vcc.voltage
    print 'mcu.vcc.u_voltage =', mcu.vcc.u_voltage
    print 'mcu.vcc.read_u_voltage() =', mcu.vcc.read_u_voltage()
    print 'mcu.vcc.read_voltage() =', mcu.vcc.read_voltage()
    print 'mcu.read_u_vcc() =', mcu.read_u_vcc()
    print 'mcu.read_vcc() =', mcu.read_vcc()
