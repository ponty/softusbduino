from memo import memoized

def asc2str(ls):
    s = ''.join(chr(i) for i in ls)
    return s

TYPE_INT8 = 1
TYPE_INT16 = 2
TYPE_INT32 = 3
TYPE_STRING = 4
TYPE_FLOAT = 5
TYPE_VOID = 6
TYPE_BYTE_ARRAY = 7

def int16_p(x):
    x = int(x)
    return [x & 0xFF, x >> 8]

class Serializer(object):
    def __init__(self, base):
        self.base = base

    def get_params(self, cmd, param1=None, param2=None, param3=None, param4=None, word=None):
        if word is not None:
            assert param3 is None
            assert param4 is None
            param3, param4 = int16_p(word)
            if param1 is None:
                param1 = 0
            if param2 is None:
                param2 = 0
        params = [cmd]
        if param1 is not None:
            params += [param1]
            if param2 is not None:
                params += [param2]
                if param3 is not None:
                    params += [param3]
                    if param4 is not None:
                        params += [param4]
        return params

    def usb_transfer(self, cmd, *args, **kw):
        params = self.get_params(cmd, *args, **kw)
        ls = self.base.usb_transfer_bytes(params)
        if not len(ls):
            return None

        def read_int(int_size):
            f = 0
            for i in range(int_size):
                try:
                    f += ls[i] << (i * 8)
                except:
                    print 'data', ls
                    raise
            return f
#        assert int_size == len(ls), 'expected size=%s data=%s' % (int_size, ls)

        typ = ls[0]
        ls = ls[1:]
        if typ == TYPE_INT8:
            x = read_int(1)
        elif typ == TYPE_INT16:
            x = read_int(2)
        elif typ == TYPE_INT32:
            x = read_int(4)
        elif typ == TYPE_STRING:
            x = asc2str(ls[:-1])
        elif typ == TYPE_BYTE_ARRAY:
            x = ls
        else:
            assert 0, 'invalid type specifier received:%s' % typ
        return x

class SerializerMixin(object):

    @property
    @memoized
    def serializer(self):
        return Serializer(self.usb)

