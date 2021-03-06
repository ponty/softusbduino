from entrypoint2 import entrypoint
from path import path
from softusbduino import version, const
from textwrap import dedent


def read_define(fname, name):
    for line in path(fname).lines():
        ls = line.split(name)
        if len(ls) > 1:
            if ls[0].strip().strip('#') == 'define':
                return ls[1].strip()


class Codegen(object):
    def __init__(self, root):
        self.root = root

    def header(self, avrlibc=True):
        s = '''
// this file was generated by codegen.py
'''
        if avrlibc:
            s += '''
// __AVR_LIBC_VERSION_STRING__ = {version}
// __AVR_LIBC_DATE_STRING__ = {date}
            \n'''.format(
                version=self.version(),
                date=self.date(),
            )

        return (s)

    def version(self):
        return read_define(self.root / 'version.h', '__AVR_LIBC_VERSION_STRING__')

    def date(self):
        return read_define(self.root / 'version.h', '__AVR_LIBC_DATE_STRING__')

    def write_header(self, hfile, text, avrlibc=True):
        print 'writing to %s' % hfile
        hfile.write_text(self.header(avrlibc) + text)

    def regs(self, target, REGISTERS_CSV):
        print '== generating code for registers =='
        valid = set()
        defs = set()
        print 'reading %s directory' % self.root
        for h in path(self.root).walkfiles('*.h'):
            for x in h.lines():
                x = x.replace('#', '').strip()
                ls = x.split() + [''] * 4
                if 'define' == ls[0]:
                    if '_struct' not in ls[1]:
                        if '_SFR_IO8' in ls[2] or '_SFR_MEM8' in ls[2]:
                            valid.add(ls[1])
                        if '_SFR_IO16' in ls[2] or '_SFR_MEM16' in ls[2]:
                            valid.add(ls[1])

                    ok = True
                    if '(' in ls[2]:
                        ok = False
                    if ls[1] != ls[1].upper():
                        ok = False
                    if ls[1].startswith('_'):
                        ok = False
                    for s in ['(', '_vect', '_H', 'eeprom']:
                        if s in ls[1]:
                            ok = False
                    if ok:
                        defs.add(ls[1])
        exlude_regs = ['SPDR0']
        valid = filter(lambda x: x not in exlude_regs, valid)
        valid = list(valid)
        valid.sort()
        TEMPLATE = '''
#ifdef {0}
    DEFINE({0})
#else
    MISSING({0})
#endif'''
        cpp = '\n'.join([TEMPLATE.format(x) for x in valid])

        self.write_header(target, cpp)

        print 'writing to %s' % REGISTERS_CSV
        REGISTERS_CSV.write_lines(valid)

    def intdefs(self, INTDEFS_CSV, target):
        print '== generating code for defines =='

        print 'reading %s' % INTDEFS_CSV
        lines = INTDEFS_CSV.text().strip().splitlines()
    #    TEMPLATE = '''
    # ifdef {0}
    #    DEFINE({0})
    # else
    #    MISSING({0})
    # endif
    #    '''
        TEMPLATE = '''DEFINE({0})'''
        cpp = '\n'.join([TEMPLATE.format(x) for x in lines])
        self.write_header(target, cpp)

    def ver(self, target):
        print '== generating code for version =='
        ls = [('SOFTUSBDUINO_VERSION', version.SOFTUSBDUINO_VERSION()),
              ('SOFTUSBDUINO_FIRMWARE_VERSION', version.SOFTUSBDUINO_FIRMWARE_VERSION),
              ]
        cpp = ''
        for name, value in ls:
            cpp += '#define %s %s \n' % (name, value)
        self.write_header(target, cpp, avrlibc=False)

    def mcu(self, target):
        print '== generating code for MCUs =='
        valid = set()
        print 'reading %s directory' % self.root
        for h in self.root.walkfiles('*.h'):
            for x in h.lines():
                x = x.replace('#', '').strip()
                x = x.replace('!', '').strip()
                ls = x.split() + [''] * 4
                if  ls[0] in ['elif', 'if']:
                    for t in ls:
                        if 'defined' in t or 'defined' in x:
                            if '__AVR_AT' in t:
                                t = t.replace('defined', '')
                                t = t.replace('(', '')
                                t = t.replace(')', '')
                                t = t.strip()
                                valid.add(t)

        valid = list(valid)
        valid.sort()
        TEMPLATE = '''
#ifdef {0}
#    ifdef MCU_DEFINED
#        error "MCU_DEFINED is already defined"
#    endif
#    define MCU_DEFINED "{0}"
#endif'''
        cpp = '\n'.join([TEMPLATE.format(x) for x in valid])
        self.write_header(target, cpp)


@entrypoint
def main():
    SoftUsb_path = path(__file__).abspath().parent.parent.parent / 'SoftUsb'
    avr_include_path = path('/usr/lib/avr/include/avr/')

    x = Codegen(avr_include_path)

    REGISTERS_CSV = path(const.REGISTERS_CSV)
    x.regs(SoftUsb_path / 'generated_registers.h', REGISTERS_CSV)

    INTDEFS_CSV = path(const.INTDEFS_CSV)
    x.intdefs(INTDEFS_CSV, SoftUsb_path / 'generated_intdefs.h')

    x.mcu(SoftUsb_path / 'generated_mcu.h')

    x.ver(SoftUsb_path / 'generated_version.h')

    print 'done'
