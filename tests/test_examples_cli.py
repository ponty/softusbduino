from easyprocess import Proc
from pyvirtualdisplay.display import Display


def filterxlib(s):
    lines = filter(lambda x: not x.startswith('Xlib:'), s.splitlines())
    return ''.join(lines)


def test_filterxlib():
    assert filterxlib('bla\nXlib:error')
    assert not filterxlib('Xlib:error')
    assert filterxlib('bla')

'''
def check_cli(mod, timeout=2):
    p = Proc('python -m softusbduino.examples.%s' % mod)
    with Display(visible=0) as d:
        p.call(timeout=timeout)
    print p
    print p.stderr
    assert not filterxlib(p.stderr)


def test_Blink():
    check_cli('proto.Blink')


def test_AnalogInOutSerial():
    check_cli('proto.AnalogInOutSerial')


def test_analogplot():
    check_cli('analogplot')


def test_simple():
    check_cli('simple')


def test_usbreset():
    check_cli('usbreset')


def test_usbreset2():
    check_cli('usbreset2')


def test_blink():
    check_cli('blink')


def test_count():
    check_cli('count')
    # reset after count!
    # otherwise timer register value is not OK
#     check_cli('reset')


def test_reset():
    check_cli('reset')


def test_guidemo():
    check_cli('guidemo', timeout=10)


def test_highfreqpwm():
    check_cli('highfreqpwm')

def test_onewire_demo():
    check_cli('onewire_demo')
'''
