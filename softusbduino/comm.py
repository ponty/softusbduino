
def asc2str(ls):
    s = ''.join(chr(i) for i in ls)
    return s

TYPE_INT8 = 1
TYPE_INT16 = 2
TYPE_INT32 = 3
TYPE_STRING = 4
TYPE_FLOAT = 5
TYPE_VOID = 6

class CommunicationMixin(object):
    def get_params(self, cmd, param1=None, param2=None, param3=None, param4=None):
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

#    def read_int(self, int_size, cmd, *args):
#        params = self.get_params(cmd, *args)
#        ls = self.read_bytes(params)
#        f = 0
#        assert int_size == len(ls), 'expected size=%s data=%s' % (int_size, ls)
#        for i in range(int_size):
#            f += ls[i] << (i * 8) 
#        return f
#    
#    def read_void(self, cmd, *args):
#        return self.read_int(0, cmd, *args)
#    
#    def read_int8(self, cmd, *args):
#        return self.read_int(1, cmd, *args)
#    
#    def read_int32(self, cmd, *args):
#        return self.read_int(4, cmd, *args)
#
#    def read_int16(self, cmd, *args):
#        return self.read_int(2, cmd, *args)
#
#    def read_string(self, cmd, *args):
#        params = self.get_params(cmd, *args)
#        ls = self.read_bytes(params)
#        return asc2str(ls)

    def read_any(self, cmd, *args):
        params = self.get_params(cmd, *args)
        ls = self.read_bytes(params)
        if not len(ls):
            return None
        
        def read_int(int_size):
            f = 0
            for i in range(int_size):
                f += ls[i] << (i * 8) 
            return f
#        assert int_size == len(ls), 'expected size=%s data=%s' % (int_size, ls)
        typ=ls[0]
        ls=ls[1:]
        if typ==TYPE_INT8:
            x=read_int(1)
        elif typ==TYPE_INT16:
            x=read_int(2)
        elif typ==TYPE_INT32:
            x=read_int(4)
        elif typ==TYPE_STRING:
            x= asc2str(ls[:-1])
        else:
            assert 0, 'invalid type specifier received:%s'%typ
        return x
