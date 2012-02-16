from bidict import bidict
from softusbduino.const import *
import logging

log = logging.getLogger(__name__)

base_divisor = {
                3:512,
                5:256,
                6:256,
                9:512,
                10:512,
                11:512,
                }
    
_div1 = bidict({
         1:1,
         2:8,
         3:64,
         4:256,
         5:1024,
         })
_div2 = bidict({
         1:1,
         2:8,
         3:32,
         4:64,
         5:128,
         6:256,
         7:1024,
         })
divisor_mapping = {
                3:_div2,
                5:_div1,
                6:_div1,
                9:_div1,
                10:_div1,
                11:_div2,
                }
timer_register = {
                3:'TCCR2B',
                5:'TCCR0B',
                6:'TCCR0B',
                9:'TCCR1B',
                10:'TCCR1B',
                11:'TCCR2B',
                }
   
timer_mask = 0b111    

#TODO: pwm_mode  read/write
#TODO: read mappings

class PwmPin(object):
    @property
    def pwm_available(self):
        return self.nr in divisor_mapping
    
    #TODO: 
    @property
    def pwm_out(self):
        raise NotImplementedError()

    @pwm_out.setter
    def pwm_out(self, x):
        self.mode = OUTPUT
        self.board.analogWrite(self.nr, x)

    @property
    def divisors_available(self):
        try:
            return divisor_mapping[self.nr].values()
        except KeyError:
            return []
        
    @property
    def divisor(self):
        if not self.pwm_available:
            return None
        d = divisor_mapping[self.nr]
#        mode = self.timer_mode
        return d[self.timer_mode]

    @divisor.setter
    def divisor(self, value):
        if not self.pwm_available:
            return None
        d = divisor_mapping[self.nr]
        self.timer_mode = d.inv[value]
    
    @property
    def timer_register_name(self):
#        self.board.digitalPinToTimer(self.nr)
        if not self.pwm_available:
            return None
        return timer_register[self.nr]

    @property
    def timer_mode(self):
        reg_name = self.timer_register_name
#        reg_id = register_ids[reg_name]
        return self.board.register_read(reg_name) & timer_mask
    
    @timer_mode.setter
    def timer_mode(self, value):
        assert value <= 7
        reg_name = self.timer_register_name
#        reg_id = register_ids[reg_name]
        old = self.board.register_read(reg_name) & ~timer_mask
        self.board.register_write(reg_name, old | value)

    @property
    def base_divisor(self):
        return base_divisor[self.nr]
        
    def calculate_pwm_frequency(self, divisor):
        return 1.0 * self.board.defines.F_CPU / self.base_divisor / divisor

    @property
    def pwm_frequencies_available(self):
        return [self.calculate_pwm_frequency(x) for x in self.divisors_available]
    
    @property
    def pwm_frequency(self):
        if not self.pwm_available:
            return None
        return self.calculate_pwm_frequency(self.divisor);

    @pwm_frequency.setter
    def pwm_frequency(self, value):
        d = divisor_mapping[self.nr]
        for x in self.divisors_available:
            f = self.calculate_pwm_frequency(x)
            if abs(f - value) <= 1:
                self.timer_mode = d.inv[x]
                return

