from nose.tools import ok_
from softusbduino.arduino import Arduino
from softusbduino.const import OUTPUT
from uncertainties import nominal_value, std_dev


def test_counter():
    mcu = Arduino()
    mcu.reset()
    p = mcu.pin(5)
    p.write_mode(OUTPUT)
    p.pwm.write_value(128)

    print 'frequencies_available:', p.pwm.frequencies_available
    for fset in p.pwm.frequencies_available:
     p.pwm.frequency = fset
     assert abs(p.pwm.frequency - fset) <= 1
     print '---------------------------'
     print 'fset=', fset
     print '---------------------------'
     for ms in [10,20,50,100,200,500,1000]:  
      for _ in range(1):
        t = ms / 1000.0

        mcu.counter.run(t)
        f = mcu.counter.frequency
        t = mcu.counter.gate_time
        err = f - fset

        print 't=%s  f=%s ' % (t,                                          f                                          )
        ok_(abs(nominal_value(err)) <= std_dev(err))



