__version__ = '1.1.7'

SOFTUSBDUINO_FIRMWARE_VERSION = 7


def SOFTUSBDUINO_VERSION():
    v = __version__
    ls = map(int, v.split('.'))
    v = 10000 * ls[0] + 100 * ls[1] + ls[2]
    return v
