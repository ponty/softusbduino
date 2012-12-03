from bunch import Bunch
from const import INTDEFS_CSV, MAGIC_NUMBER
from path import path
from memo import memoized

INTDEFS_CSV = path(INTDEFS_CSV)

# class Define(object):
#    def __init__(self, base, name):
#        self.base = base
#        self.name = name
#
#    @property
#    def value(self):
#        return self.base.value(self.name)
#
#    @property
#    def exists(self):
#        return self.base.exists(self.name)


class DefineError(Exception):
    pass


def _intdef_ids():
    intdef_ids = Bunch([(x, i) for i, x in enumerate(
        INTDEFS_CSV.lines(retain=False)) if x.strip()])
    return intdef_ids


class Defines(object):
    intdef_ids = _intdef_ids()

    special_defines = Bunch(
        __TIME__=22,
        __DATE__=23,
        MAGIC_NUMBER=MAGIC_NUMBER,
        MCU_DEFINED=26,
        USBDRV_VERSION=25,
        USB_CFG_IOPORT=34,  # A -> 1
    )

    def __init__(self, base):
        self.base = base

    def exists(self, name):
        try:
            self.value(name)
            return True
        except DefineError:
            return False

    def as_dict(self):
        d = dict()
        for name in self.intdef_ids:
            d[name] = self.value(name)
        for name in self.special_defines.keys():
            d[name] = self.value(name)
        return d

    @memoized
    def value(self, name):
        try:
            def_id = self.intdef_ids[name]
            value = self.base.read_int_define(def_id)
        except KeyError:
            try:
                def_id = self.special_defines[name]
                value = self.base.read_special_define(def_id)
            except KeyError:
                raise DefineError('define not found: %s' % name)
        return value

#    def __getattr__(self, name):
#        value = self.read_define(name)
#        if value is not None:
#            return value
#        else:
#            return object.__getattribute__(self, name)


class DefinesLowLevel(object):
    def __init__(self, base):
        self.base = base

    def read_int_define(self, def_id):
        return self.base.usb_transfer(51, def_id)

    def read_special_define(self, def_id):
        return self.base.usb_transfer(def_id)


class DefineMixin(object):

    @property
    @memoized
    def lowlevel_defines(self):
        return DefinesLowLevel(self.serializer)

    @property
    @memoized
    def defines(self):
        return Defines(self.lowlevel_defines)

    @memoized
    def define(self, name):
        return self.defines.value(name)
#        return Define(self.defines, name)
