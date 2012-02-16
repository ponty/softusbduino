from path import path

false = 0
true = 1
LOW = false
HIGH = true
OUTPUT = HIGH
INPUT = LOW
#EXTERNAL=0
DEFAULT = 1
INTERNAL = 3

#INPUT = Symbol('INPUT', __name__)
#OUTPUT = Symbol('OUTPUT', __name__)

REGISTER_CHECK = 1
REGISTER_READ = 2
REGISTER_WRITE = 3
REGISTER_ADDRESS = 4
REGISTER_MISSING = 111
REGISTER_OK = 222

MAGIC_NUMBER = 42


ID_VENDOR = 0x16c0
ID_PRODUCT = 0x05df

REGISTERS_CSV = path(__file__).abspath().parent / 'generated_registers.csv'
INTDEFS_CSV = path(__file__).abspath().parent / 'intdefs.csv'
