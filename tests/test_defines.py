from nose.tools import eq_, ok_
from softusbduino.arduino import Arduino
from softusbduino.defines import DefineError
from config import F_CPU
from util import exc_

dev = None


def setup():
    global dev
    dev = Arduino()
    dev.reset()


def teardown():
    global dev
    dev.reset()


def test_defs():
#    eq_(dev.defines.A0, 14)

    eq_(dev.define('A0'), 14)
    eq_(dev.defines.value('A0'), 14)

#    ok_(dev.define('xx'))
    exc_(DefineError, lambda: dev.define('xx'))
    exc_(DefineError, lambda: dev.defines.value('xx'))

    eq_(dev.defines.exists('A0'), True)
    eq_(dev.defines.exists('xx'), False)

#    exc_(DefineError,dev.define('xx'))

    d = dev.defines.as_dict()
    eq_(d['A0'], 14)
    ok_(len(d) > 20)


def test_defines():
    eq_(dev.define('A0'), 14)
    eq_(dev.define('ARDUINO'), 22)
    eq_(dev.define('MAGIC_NUMBER'), 42)
    eq_(dev.define('F_CPU'), F_CPU)

    eq_(dev.defines.as_dict()['A0'], 14)

    for x in dev.defines.as_dict():
        assert x.strip(), 'empty define:-->%s<--' % x
