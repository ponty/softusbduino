from softusbduino.const import *
from softusbduino.pwmpin import PwmPin
from uncertainties import ufloat
import logging

log = logging.getLogger(__name__)


class Pin(PwmPin):
    @classmethod
    def all_pins(cls, board, kind='all'):
        return [Pin(board, x) for x in board.pinRange(kind=kind)]
                    
    def __init__(self, board, nr=None):
        self._pullup = False
        self.board = board
        A0 = self.board.defines.A0
        if isinstance(nr, basestring):
            if nr[0] == 'D':
                nr = int(nr[1:])
            elif nr[0] == 'A':
                nr = int(nr[1:]) + A0
            
#        if nrAnalog is not None:
#            nr = nrAnalog + self.board.defines.A0
        self.nr = int(nr)
        self.digital = self.nr < A0
        self.analog = not self.digital
        

    @property
    def name(self):
        if self.digital:
            return 'D%s' % self.nr
        else:
            return 'A%s' % self.nrAnalog
            
            
    @property
    def nrAnalog(self):
        x = self.nr - self.board.defines.A0
        if x >= 0:
            return x
    
    @property
    def dig_in(self):
        if self.mode == INPUT:
            return self.board.digitalRead(self.nr)

    @property
    def dig_out(self):
        if self.mode == OUTPUT:
            return self.board.digitalRead(self.nr)
    
    @dig_out.setter
    def dig_out(self, x):
        self.mode = OUTPUT
        self.board.digitalWrite(self.nr, x)
        
    @property
    def mode(self):
        return self.board.readPinMode(self.nr)

    @mode.setter
    def mode(self, x):
        assert self.nr != self.board.usbMinusPin
        assert self.nr != self.board.usbPlusPin
        if x == 'INPUT':
            x = INPUT
        if x == 'OUTPUT':
            x = OUTPUT
        self.board.pinMode(self.nr, x)
        if x == INPUT:
            self.board.digitalWrite(self.nr, self._pullup)

    
    @property
    def pullup(self):
        #        TODO: read 
        return self._pullup
#        if self.mode == INPUT:
#            raise NotImplementedError()

    @pullup.setter
    def pullup(self, x):
        x = bool(x)
        if self.mode == INPUT:
            if self._pullup != x:
                self.board.digitalWrite(self.nr, x)
        self._pullup = x
#        self.mode = INPUT

    @property
    def an_in(self):
#        if self.analog and self.mode == INPUT:
        return self.analogRead()
    @property
    def u_an_in(self):
#        if self.analog and self.mode == INPUT:
        return ufloat((self.analogRead(), self.board.adc_accuracy))

    def analogRead(self):
        x = self.board.analogRead(self.nr)
#        log.debug('analogRead:%s @%s'%(x,self.nr))
        return x
    
    def analogWrite(self, value):
        return self.board.analogWrite(self.nr, value)
        
    @property
    def programming_function(self):
        if self.nr == self.board.defines.MISO:
            return 'MISO'
        if self.nr == self.board.defines.MOSI:
            return 'MOSI'
        if self.nr == self.board.defines.SCK:
            return 'SCK'
        if self.nr == self.board.defines.SS:
            return 'SS'
            
    def reset(self):
        self.mode = INPUT
