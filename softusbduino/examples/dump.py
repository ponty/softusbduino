from dicts.sorteddict import SortedDict
from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
import inspect


def dump(obj):
    for attr in dir(obj):
        if not attr.startswith('__'):
            if not inspect.ismethod(getattr(obj, attr)):
                if not attr in 'registers defines device register_ids'.split():
                    print "%-15s = %15s" % (attr, getattr(obj, attr))

@entrypoint
def usbdump():
    print
    print '========================='
    print 'attributes:'
    print '========================='
    board = Arduino()
    dump(board) 
    print
    
    print
    print '========================='
    print 'defines:'
    print '========================='
    for k, v in SortedDict(board.defines.dump()).items():  
        print '%-20s = %18s' % (k, v)

    print
    print '========================='
    print 'registers:'
    print '========================='
    for k, v in SortedDict(board.registers.dump()).items():  
        print '%-20s = 0x%02X @0x%2X' % (k, v[1],v[0],)
        







  
