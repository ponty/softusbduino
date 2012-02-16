from bunch import Bunch
from softusbduino.const import REGISTER_CHECK, REGISTER_OK, REGISTER_MISSING, \
    REGISTER_READ, REGISTER_WRITE, REGISTER_ADDRESS
from const import REGISTERS_CSV
from path import path

REGISTERS_CSV=path(REGISTERS_CSV)

def int16_p(x):
    return [x & 0xFF, x >> 8]      

class Register(object):    
    def __init__(self, board, name):
        self.board = board
        self.name = name
        
    @property
    def address(self):        
        return self.board.register_address(self.name)
        
    @property
    def available(self):        
        return self.board.register_check(self.name)
    
    @property
    def value(self):
        return self.board.register_read(self.name)
        
    @value.setter
    def value(self, value):
        return self.board.register_write(self.name, value)

class Registers(object):    
    def __init__(self, board):
        self.__dict__['board'] = board
#        self.board = board
        
    def reg_id(self,reg_name):
        board=object.__getattribute__(self, 'board')
        reg_id = board.register_ids[reg_name]
        return reg_id

    def dump(self):
        d = Bunch()
        for name, reg_id in self.board.register_ids.items():
            if self.board.register_check(name):
                value = self.board.register_read(name)
                address = self.board.register_address(name)
                d[name] = (address, value)
            else:
                value = None
        return d
        
    def __getattr__(self, name):
        try:
            reg_id = self.reg_id(name)
            if reg_id is not None:
                return self.board.register_read(name)
        except KeyError:
            return object.__getattribute__(self, name)
    def __setattr__(self, name, value):
        reg_id = self.reg_id(name)
        if reg_id is not None:
            return self.board.register_write(name, value)
        else:
            self.__dict__[name] = value

class ArduinoUsbRegisterError(Exception):
    pass


def _register_ids():
    return Bunch([(x, i) for i, x in enumerate(REGISTERS_CSV.lines(retain=False))])

class RegisterMixin(object):    
    register_ids = _register_ids()

    def register_check(self, reg_name):
        reg_id = self.register_ids[reg_name]
        x = self.read_any(50, *int16_p(reg_id) + [ REGISTER_CHECK])
        if x == REGISTER_OK:
            return True
        if x == REGISTER_MISSING:
            return False
        raise ArduinoUsbRegisterError('invalid code')
    
    def reg_id(self,reg_name):
        reg_id = self.register_ids[reg_name]
        return reg_id
    
    def register_read(self, reg_name):
        reg_id = self.reg_id(reg_name)
        return self.read_any(50, *int16_p(reg_id) + [ REGISTER_READ])
    
    def register_write(self, reg_name, value):
        reg_id = self.reg_id(reg_name)
        self.read_any(50, *int16_p(reg_id) + [ REGISTER_WRITE, value])
    
    def register_address(self, reg_name):
        reg_id = self.reg_id(reg_name)
        return self.read_any(50, *int16_p(reg_id) + [ REGISTER_ADDRESS]) 


    def register(self, name):
        if not self.reg_id(name):
            # unknown
            return None
        if not self.register_check(name):
            # missing
            return None
        return Register(self, name)
    
