from memo import memoized
from softusbduino.const import *
import logging
import time

log = logging.getLogger(__name__)

class OneWireError(Exception):
    pass

def crc8(ls):
    crc = 0
    for x in ls:
        for _ in range(8) :
            mix = (crc ^ x) & 0x01
            crc >>= 1
            if (mix):
                crc ^= 0x8C
            x >>= 1
    return crc

class LowLevel1Wire(object):
    def __init__(self, base):
        self.base = base

    def init_1wire(self, index, pin):
        return self.base.usb_transfer(62, index, pin)

    def reset_search(self, index):
        return self.base.usb_transfer(64, index)

    def search(self, index):
        return self.base.usb_transfer(65, index)

    def reset(self, index):
        return self.base.usb_transfer(66, index)

    def select(self, index):
        return self.base.usb_transfer(67, index)

    def write_byte(self, index, value, power=0):
        return self.base.usb_transfer(68, index, value, power)

    def depower(self, index):
        return self.base.usb_transfer(69, index)

    def read_address(self):
        return self.base.usb_transfer(70)

    def write_address_low(self, ls):
        return self.base.usb_transfer(71, *ls)

    def write_address_high(self, ls):
        return self.base.usb_transfer(72, *ls)

    def read_slow_value(self):
        return self.base.usb_transfer(200)

    def read_byte(self, index):
        return self.base.usb_transfer(73, index)

resolution_configs = {
 0x00:9,
 0x20:10,
 0x40:11,
 0x60:12,
 }


class Scratchpad(object):
    device = None
    data = None
    t = None

    # TODO:
    # 85 Celsius is often an error for DS18B20
    # http://mango.serotoninsoftware.com/forum/posts/list/247.page
    ignore85C = True

    def __init__(self, device):
        self.device = device
        self.read()

    def read(self):
        self.t = time.time()
        self.data = self.device._read_scratchpad()

    @property
    def celsius(self):
        data = self.data
        if not data:
            return
        raw = (data[1] << 8) | data[0]
        celsius = raw / 16.0
        if self.ignore85C and celsius == 85:
            return None
        return celsius

    @property
    def resolution(self):
        data = self.data
        if not data:
            return
        cfg = (data[4] & 0x60)
        x = resolution_configs[cfg]
        assert x in [9, 10, 11, 12]
        return x

    @property
    def connected(self):
        return bool(self.data)


class Device1Wire(object):
    known_chips = {
    0x10:"DS18S20",
    0x28:"DS18B20",
    0x22:"DS1822",
                 }

    def __init__(self, bus, address):
        self.address = address
        self.address_str = '.'.join(['%02X' % x for x in address])
        self.bus = bus
        self.chip = self.known_chips.get(self.address[0], None)
        self.address_valid = address[7] == crc8(address[:7])

    def select(self):
        self.bus.select(self.address);

    _resolution = None

    @property
    def resolution(self):
        if not self._resolution:
            self._read_scratchpad()
        return self._resolution

    def parasite(self):
        self.bus.reset()
        self.select()
        self.bus.write(0xB4)
        x = self.bus.read_bit()
        self.bus.reset()
        return not x

    def scratchpad(self):
        return Scratchpad(self)

    def _read_scratchpad(self):
        self.bus.reset();
        self.select();
        self.bus.write_byte(0x44) #start conversion

        time.sleep(1)

        self.bus.reset();
        self.select();
        self.bus.write_byte(0xBE); # Read Scratchpad

        data = []
        for i in range(9):
            d = self.bus.read_byte();
            data.append(d);

        self.bus.reset();

        valid = data[8] == crc8(data[:8])
        if not valid:
            raise OneWireError('invalid crc')

        cfg = (data[4] & 0x60);
        self._resolution = resolution_configs[cfg]
        assert self._resolution in [9, 10, 11, 12]

        return data


class Bus1Wire(object):

    index = 0

    def __init__(self, base, pin):
        self.pin = pin
        self.base = base

        self.index = Bus1Wire.index
        Bus1Wire.index += 1

#        assert self.index < self.mcu.defines.ONEWIRE_BUS_COUNT
        self.base.init_1wire(self.index, pin.nr)

#    @property    
#    def mcu(self):
#        return self.pin.mcu

    def search(self):
        ls = []
        self.base.reset_search(self.index)
        while 1:
            self.base.search(self.index)
            time.sleep(0.1)
            ok = self.base.read_slow_value()
            if not ok:
                break
            a = self.base.read_address()

            # break in case of infinite loop
            if a in [x.address for x in ls]:
                break

            # skip 00:00:00:00:00:00:00:00
            if sum(a) == 0:
                break

            ls.append(Device1Wire(self, a))
        return ls

    def reset(self):
        self.base.reset(self.index)
        time.sleep(0.1)
        return self.base.read_slow_value()

    def write_byte(self, value):
        self.base.write_byte(self.index, value, power=1)
        time.sleep(0.1)

    def read_byte(self):
        self.base.read_byte(self.index)
        time.sleep(0.1)
        return self.base.read_slow_value()

    def select(self, address):
        self.base.write_address_low(address[:4])
        self.base.write_address_high(address[4:])
        self.base.select(self.index);
        time.sleep(0.1)

class OneWire(object):
    def __init__(self, base, defines, mcu):
        self.base = base
        self.defines = defines
        self.mcu = mcu

    @property
    def available(self):
        return bool(self.defines.value('HAS_ONE_WIRE'))

    @memoized
    def _bus(self, pin):
        return Bus1Wire(self.base, pin=pin)

    def bus(self, pin_nr):
        if not self.available:
            raise OneWireError('OneWire library is not available in firmware')
        return self._bus(self.mcu.pin(pin_nr))


class OneWireMixin(object):

    @property
    @memoized
    def onewire(self):
        return OneWire(self.lowlevel_1wire, self.defines, self)


    @property
    @memoized
    def lowlevel_1wire(self):
        return LowLevel1Wire(self.serializer)




