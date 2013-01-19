from uncertainties import ufloat
import logging
import time

log = logging.getLogger(__name__)


class AnalogIn(object):
    pin = None
    value = None
    t = None

    def __init__(self, pin):
        self.pin = pin

    def read(self):
        self.t = time.time()
        self.value = self.pin.read_analog()
        return self

    @property
    def u_value(self):
        return ufloat((self.value, self.pin.mcu.adc_accuracy))

    @property
    def voltage(self):
        return self.u_voltage.nominal_value

    @property
    def u_voltage(self):
        return self.u_value / 1023.0 * self.pin.mcu.vcc.voltage

    def __repr__(self):
        return 'AnalogIn<value:%s voltage:%s>' % (self.value, self.voltage)

    def asdict(self):
        return dict(t=self.t, analog_value=self.value, voltage=self.voltage)


class DigitalIn(object):
    pin = None
    value = None
    t = None

    def __init__(self, pin):
        self.pin = pin

    def read(self):
        self.t = time.time()
        self.value = self.pin.read_digital()
        return self

    def __repr__(self):
        return 'DigitalIn<value:%s>' % (self.value)
