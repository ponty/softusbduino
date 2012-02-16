from bunch import Bunch
from const import INTDEFS_CSV, MAGIC_NUMBER
from path import path

INTDEFS_CSV = path(INTDEFS_CSV)


class Defines(object):    
    intdef_ids = Bunch([(x, i) for i, x in enumerate(INTDEFS_CSV.lines(retain=False)) if x.strip()])
    
    special_defines = Bunch(
            __TIME__=22,
            __DATE__=23,
            MAGIC_NUMBER=MAGIC_NUMBER,
            MCU_DEFINED=26,
            USBDRV_VERSION=25,
            USB_CFG_IOPORT=34, # A -> 1
           )



    def __init__(self, board):
        self.board = board
        
    def dump(self):
        d = dict()
        for name in self.intdef_ids:
            d[name] = self.__getattr__(name)
        for name in self.special_defines.keys():
            d[name] = self.__getattr__(name)
        return d
    
    def read_define(self, name):
        try:
            reg_id = self.intdef_ids[name]
            value = self.board.read_int_define(reg_id)
        except KeyError:
            try:
                reg_id = self.special_defines[name]
                value = self.board.read_special_define(reg_id)
            except KeyError:
                return None
        return value
    
    def __getattr__(self, name):
        value = self.read_define(name)
        if value is not None:
            return value
        else:
            return object.__getattribute__(self, name)
