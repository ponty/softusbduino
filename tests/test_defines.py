from nose.tools import eq_, ok_
from softusbduino.arduino import Arduino
from softusbduino.defines import DefineError
from util import exc_
from config import config

dev = None


def setup():
    global dev
    dev = Arduino()
    dev.pins.reset()


def teardown():
    global dev
    dev.pins.reset()


def test_defs():
#    eq_(dev.defines.A0, config.A0)

    eq_(dev.define('A0'), config.A0)
    eq_(dev.defines.value('A0'), config.A0)

#    ok_(dev.define('xx'))
    exc_(DefineError, lambda: dev.define('xx'))
    exc_(DefineError, lambda: dev.defines.value('xx'))

    eq_(dev.defines.exists('A0'), True)
    eq_(dev.defines.exists('xx'), False)

#    exc_(DefineError,dev.define('xx'))

    d = dev.defines.as_dict()
    eq_(d['A0'], config.A0)
    ok_(len(d) > 20)


def test_defines():
    eq_(dev.define('A0'), config.A0)
    eq_(dev.define('ARDUINO'), config.ARDUINO)
    eq_(dev.define('MAGIC_NUMBER'), config.MAGIC_NUMBER)
    eq_(dev.define('F_CPU'), config.F_CPU)
    # ok_('ATmega' in dev.define('MCU_DEFINED'))
    eq_(dev.define('MCU_DEFINED'), config.MCU_DEFINED)

    eq_(dev.defines.as_dict()['A0'], config.A0)

    for x in dev.defines.as_dict():
        assert x.strip(), 'empty define:-->%s<--' % x


def test_model():
    eq_(dev.model, config.model)
