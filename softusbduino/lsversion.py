import platform
from entrypoint2 import entrypoint

@entrypoint
def list_versions():
    ''' print versions
    '''

    TEMPLATE='{0:<15} {1}'
    print TEMPLATE.format('platform', platform.platform())
    print TEMPLATE.format('python', platform.python_version())
    





