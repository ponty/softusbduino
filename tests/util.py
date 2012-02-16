

def exc_(excClass, callableObj, *args, **kwargs):
    """Fail unless an exception of class excClass is thrown
       by callableObj when invoked with arguments args and keyword
       arguments kwargs. If a different type of exception is
       thrown, it will not be caught, and the test case will be
       deemed to have suffered an error, exactly as for an
       unexpected exception.
    """
    try:
        callableObj(*args, **kwargs)
    except excClass:
        return
    else:
        if hasattr(excClass, '__name__'): 
            excName = excClass.__name__
        else: 
            excName = str(excClass)
        raise Exception("%s not raised" % excName)
