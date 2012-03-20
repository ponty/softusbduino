from entrypoint2 import entrypoint
from softusbduino.const import OUTPUT, INPUT
from softusbduino.pin import Pin
from softusbduino.arduino import Arduino
from back import BackgroundHandler
from traits.has_traits import HasTraits
from traits.trait_types import Str, Any, List, Instance, Enum, Bool, Range, Int
from traitsui.editors.list_editor import ListEditor
from traitsui.editors.range_editor import RangeEditor
from traitsui.editors.table_editor import TableEditor
from traitsui.group import HGroup, Tabbed, Group
from traitsui.item import Item
from traitsui.view import View
import time
                               
class Define(HasTraits):
    name = Str()
    value = Any()

class PinWrapper(HasTraits):
    pin = Instance(Pin)
    function = Any()
    usb = Any()
    timer = Any()
    def _pin_changed(self):
        self.name = self.pin.name
        self.mode = ['INPUT', 'OUTPUT'][self.pin.read_mode()]
        self.digital_output = bool(self.pin.read_digital())
        self.function = self.pin.programming_function
        self.usb = ['','+','-'][self.pin.is_usb_plus+2*self.pin.is_usb_minus]
        self.avr_pin = self.pin.avr_pin
        
        if self.pin.pwm.available:
            ls = [int(x) for  x in self.pin.pwm.frequencies_available]
            self.add_trait('pwm_frequency', Enum(ls))
            self.pwm_frequency = int(self.pin.pwm.frequency) 
            self.timer = self.pin.pwm.timer_register_name
        
    def _pwm_frequency_changed(self):
        self.pin.pwm.frequency = self.pwm_frequency
    
    pwm_output = Range(0, 255)
    def _pwm_output_changed(self):
        self.pin.pwm.write_value(self.pwm_output)
        
    pwm = Bool()
    def _pwm_changed(self):
        if self.pwm:
            self._pwm_output_changed()
        else:
            self._digital_output_changed()
        
    name = Str()
    mode = Enum(['INPUT', 'OUTPUT'])
    def _mode_changed(self):
        self.pin.write_mode(OUTPUT if (self.mode == 'OUTPUT') else INPUT)
    pullup = Bool()
    def _pullup_changed(self):
        self.pin.write_pullup(self.pullup)
    digital_input = Bool()
    digital_output = Bool()
    def _digital_output_changed(self):
        self.pin.write_digital(self.digital_output)
    analog_input = Any()
    voltage = Any()
    
    def update(self):
        an = self.pin.read_analog_obj()
        
        self.analog_input = an.value
        self.voltage = an.voltage
        
        self.digital_input = bool(self.pin.read_digital_in())
        
    traits_view = View(
            HGroup(
                     Item('name',
                          show_label=False,
                          style='readonly',
                              ),
                     Item('avr_pin',
                          show_label=False,
                          style='readonly',
                        format_func=lambda x:'(%s)'%(x),

                              ),
            'mode',
                     Item('pwm',
                          visible_when='mode=="OUTPUT"',
                          defined_when='pin.pwm.available',
                              ),
            HGroup(
                     Item('digital_input',
                          defined_when='pin.is_digital',
                          enabled_when='0',
                              ),
                     Item('analog_input',
                          defined_when='pin.is_analog',
                          style='readonly',
                              ),
                     Item('voltage',
                          defined_when='pin.is_analog',
                          style='readonly',
                              ),
                     Item('pullup',
                              ),
                  visible_when='mode=="INPUT"',
                  ),
                     Item('digital_output',
                            visible_when='mode=="OUTPUT" and not pwm',
                              ),
            HGroup(
                     Item('pwm_frequency',
                              ),
                     Item(name='pwm_output',
                          editor=RangeEditor(
                              mode='slider',
                              low=0,
                              high=255,
                              ),
                          style='custom',
                              ),
                  visible_when='mode=="OUTPUT" and pwm',
                  defined_when='pin.pwm.available',
                  ),
                 Item('timer',
                      defined_when='timer',
                      style='readonly',
                          ),
                 Item('function',
                      defined_when='function',
                      style='readonly',
                          ),
                 Item('usb',
                      defined_when='usb',
                      style='readonly',
                          ),
            ),
            )
    

class Handler (BackgroundHandler):
    def loop(self):
        ''
        self.info.object.update()
        
class BoardWrapper(HasTraits):
    mcu = Any
    pins = List(PinWrapper)
    digital_pins = List(PinWrapper)
    analog_pins = List(PinWrapper)
    def _mcu_changed(self):
        mcu = self.mcu
        s = [Define(name=k, value=v) for k, v in self.mcu.defines.as_dict().items()]
        s.sort(key=lambda x:x.name)
        self.defines = s
        self.digital_pins = [PinWrapper(pin=mcu.pin(x)) for x in mcu.pins.range_digital]
        self.analog_pins = [PinWrapper(pin=mcu.pin(x)) for x in mcu.pins.range_analog]
        self.pins = self.digital_pins + self.analog_pins
        
#    x = Str()
    defines = List(Define)
    update_interval = Int(1000, desc='interval in msec')
    def update(self):
        for x in self.pins:
            x.update()
        time.sleep(self.update_interval / 1000.0)

    traits_view = View(
      Tabbed(
#        HGroup(
             Item(name='digital_pins',
                  editor=ListEditor(
                                    style='custom',
                                    ),
                        style='readonly',
                      show_label=False,
#                      width=400,
#                      height=600,
                  ),
             Item(name='analog_pins',
                  editor=ListEditor(
                                    style='custom',
                                    ),
                        style='readonly',
                      show_label=False,
#                      width=400,
#                      height=600,
                  ),
#             ),
#                   ),
             Group(
             Item(name='update_interval',
                  editor=RangeEditor(
                      mode='slider',
                      low=1,
                      high=1000,
                      ),
                  style='custom',
                      ),
                   label='settings',
                   ),
             Item('defines',
                  show_label=False,
                  editor=TableEditor(
                                   auto_size=False,
                                   editable=False,
                                   configurable=False,
                                   ),
                 style='readonly',
                                           )
                             ),
                     
                buttons=[ 'Undo', 'Revert', 'OK', 'Cancel' ],
                kind='live',
                resizable=True,
                handler=Handler(),
                     )
        

@entrypoint
def main(pin='', pullup=0):
    '''
    
    
    :param pin: examples: 'D0','A2'
    
    '''
    mcu = Arduino(reset=False)
    if pin:
        pin = mcu.pin(pin)
        if pullup:
            pin.pullup = pullup
    
    BoardWrapper(mcu=mcu).configure_traits()



