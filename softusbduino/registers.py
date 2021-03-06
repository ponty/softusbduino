from bunch import Bunch
from const import REGISTERS_CSV, REGISTER_SIZE
from memo import memoized
from softusbduino.const import REGISTER_CHECK, REGISTER_OK, REGISTER_MISSING, \
    REGISTER_READ, REGISTER_WRITE, REGISTER_ADDRESS
from util import lines
# from path import path

# REGISTERS_CSV = path(REGISTERS_CSV)

# def int16_p(x):
#    return [x & 0xFF, x >> 8]


class Register(object):
    def __init__(self, base, name):
        self.base = base
        self.name = name

    @property
    @memoized
    def address(self):
        return self.base.address(self.name)

    @property
    @memoized
    def exists(self):
        return self.base.exists(self.name)

    def read_value(self):
        return self.base.read_value(self.name)

    def write_value(self, value):
        return self.base.write_value(self.name, value)
    value = property(read_value, write_value)

    @property
    @memoized
    def size(self):
        return self.base.size(self.name)


class RegisterError(Exception):
    pass


def _register_id_map():
    return Bunch([(x, i) for i, x in enumerate(lines(REGISTERS_CSV))])


class RegistersLowLevel(object):
    def __init__(self, base):
        self.base = base

    def read_value(self, reg_id):
        return self.base.usb_transfer(102, word1=reg_id)

    def write_value(self, reg_id, value):
        self.base.usb_transfer(103, word1=reg_id, word2=value)

    def read_address(self, reg_id):
        return self.base.usb_transfer(104, word1=reg_id)

    def read_exists(self, reg_id):
        return self.base.usb_transfer(101, word1=reg_id)

    def read_size(self, reg_id):
        return self.base.usb_transfer(105, word1=reg_id)


class RegistersProxy(object):
    def __init__(self, base):
        self.base = base
#    def __init__(self, mcu):
#        self.__dict__['mcu'] = mcu
#        self.mcu = mcu

#    def reg_id(self, reg_name):
#        mcu = object.__getattribute__(self, 'mcu')
#        reg_id = mcu.register_ids[reg_name]
#        return reg_id

#    def dump(self):
#        d = Bunch()
#        for name, reg_id in self.mcu.register_ids.items():
#            if self.mcu.register_check(name):
#                value = self.mcu.register_read(name)
#                address = self.mcu.register_address(name)
#                d[name] = (address, value)
#            else:
#                value = None
#        return d

    def __getattr__(self, name):
        if name == 'base':
            return object.__getattribute__(self, name)

        if self.base.exists(name):
            return self.base.read_value(name)
        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name == 'base':
            self.__dict__[name] = value

        if self.base.exists(name):
            return self.base.write_value(name, value)
        else:
            self.__dict__[name] = value


class Registers(object):
    def __init__(self, base):
        self.base = base

    @property
    @memoized
    def proxy(self):
        return RegistersProxy(self)

    @property
    @memoized
    def  register_id_map(self):
        return _register_id_map()

    @memoized
    def exists(self, reg_name):
        reg_id = self._id(reg_name)
        if reg_id is None:
            return False

        x = self.base.read_exists(reg_id)

        if x == REGISTER_OK:
            return True
        if x == REGISTER_MISSING:
            return False
        raise RegisterError('invalid code: %s' % x)

    @memoized
    def size(self, reg_name):
        reg_id = self._check_name(reg_name)
        return self.base.read_size(reg_id)

    def _id(self, reg_name):
        reg_id = self.register_id_map.get(reg_name, None)
        return reg_id

    def _check_name(self, reg_name):
        if not self.exists(reg_name):
            raise RegisterError('missing register: %s' % str(reg_name))
        return self._id(reg_name)

    def read_value(self, reg_name):
        reg_id = self._check_name(reg_name)
        return self.base.read_value(reg_id)

    def write_value(self, reg_name, value):
        reg_id = self._check_name(reg_name)
        self.base.write_value(reg_id, value)

    @memoized
    def address(self, reg_name):
        reg_id = self._check_name(reg_name)
        return self.base.read_address(reg_id)

    def as_dict(self):
        d = dict()
        for name, reg_id in self.register_id_map.items():
            if self.exists(name):
                d[name] = self.read_value(name)
        return d


class RegisterMixin(object):

    @property
    @memoized
    def lowlevel_registers(self):
        return RegistersLowLevel(self.serializer)

    @property
    @memoized
    def registers(self):
        return Registers(self.lowlevel_registers)

    @memoized
    def register(self, name):
#        if not self.register_id(name):
#            # unknown
#            raise RegisterError('unknown register: %s (check %s)' % (name, REGISTERS_CSV))
#            return None
#        if not self.register_check(name):
#            # missing
#            raise RegisterError('missing register: %s' % (name,))
#            return None
        return Register(self.registers, name)
