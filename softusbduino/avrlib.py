from confduino.util import tmpdir
from path import path
from scipy.weave.build_tools import CompileError
from scipy.weave.inline_tools import inline
import tempfile

# 'UDR0' can be bit or byte on differrent MCUs
# just skip it (no better easy solution)
# ignore = ['UDR0']


def tmpdir(dir=None, suffix=''):
    x = tempfile.mkdtemp(suffix=suffix, prefix='confduino_', dir=dir)
    return path(x)


def clone_avrlib():
    d = tmpdir()
    path('/usr/lib/avr/include/avr').copytree(d / 'avr')
    return d


def avr_define_value(define, mcu):
#    if define in ignore:
#        return None
    code = """
    #include <avr/io.h>
    #ifdef %s
    return_val = %s;
    #endif
    """ % (define, define)
#    try:
    x = inline(code,
               verbose=0,
               force=1,
               define_macros=[(mcu, None)],
               include_dirs=[clone_avrlib()],
               #                  language='c',
               )

    return x
#    except CompileError:
#        pass


def avr_define_value_list(defines, mcu):
    N = len(defines)
    templ = '''
        #ifdef %(define)s
        ret[%(i)s] = %(define)s;
        #endif
    '''
    ls = [templ % dict(define=x, i=i) for i, x in enumerate(defines)]
    ifdefcode = '\n'.join(ls)
    code = r'''
    # include <avr/io.h>

    py::list ret;
    for(int i = 0; i < N; i++)
    {
        ret.append(py::None);
    }
    %s

    return_val = ret;
    ''' % ifdefcode
#    print code

    values = inline(code,
                    arg_names=['N', 'defines'],
                    verbose=1,
                    force=1,
                    define_macros=[(mcu, None)],
                    include_dirs=[clone_avrlib()],
                    #                  language='c',
                    )
#    print 555,x
#    dic=dict( [(n,v) for n,v in zip(names, values) if v is not None])

    return values
