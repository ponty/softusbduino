from memo import memoized
from uncertainties import ufloat
import time


class Vcc(object):
    base = None
    _u_voltage = None
    t = None

    def __init__(self, base):
        self.base = base
        self.read_voltage()

    def read_voltage(self):
        self.t = time.time()
        self._u_voltage = self.base.read_u_vcc()
        return self.voltage

    def read_u_voltage(self):
        self.read_voltage()
        return self.voltage

    def  get_u_voltage(self):
        return self._u_voltage

    def  set_u_voltage(self, V):
        self._u_voltage = ufloat(V)
    u_voltage = property(get_u_voltage, set_u_voltage)

    def  get_voltage(self):
        return self.u_voltage.nominal_value

    def  set_voltage(self, V):
        self._u_voltage = ufloat((V, 0))
    voltage = property(get_voltage, set_voltage)


class VccMixin(object):

    @property
    @memoized
    def vcc(self):
        x = Vcc(self)
        return x

    def  read_vcc(self):
        return self.read_u_vcc().nominal_value

    def  read_u_vcc(self):
        '''
        Vcc with uncertainty
        '''
        reg=self.registers.proxy

        reg.ADMUX = 0x4E  # 0b01001110
        time.sleep(0.002)  # Wait for Vref to settle
        reg.ADCSRA |= 0x40  # 0b01000000
        while reg.ADCSRA & 0x40:
            time.sleep(0.001)
        result = reg.ADCL | (reg.ADCH << 8)
        error = self.adc_accuracy
        u_result = ufloat((result, error))
        result = (self.bandgap_voltage * 1023L) / u_result

        return result
