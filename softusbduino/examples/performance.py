from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
import time


def measure(board,n, f):
    start = time.time()
    for x in range(n):
        exec 'board.'+f
    dt = time.time() - start
    print '%-35s %8.2f ms per call, %5.0f call per second' % (f,1000.0 * dt / n, 1.0 / dt * n)

@entrypoint
def main(n=100):
    board = Arduino()

    print 'performance test'
    print 'n=', n
    print
    measure(board,n, 'analogRead(0)')    
    measure(board,n, 'pinMode(8,0)')    
    measure(board,n, 'digitalRead(8)')    
    measure(board,n, 'digitalPinToBitMask(0)')    
    measure(board,n, 'digitalPinToPort(0)')    
    measure(board,n, 'portModeRegister(0)')    
    measure(board,n, 'defines.read_define("__TIME__")')    
    measure(board,n, 'defines.read_define("MCU_DEFINED")')    
    measure(board,n, 'readPinMode(0)')    
    measure(board,n, 'vcc')    
    measure(board,n, 'pinCount')    
    measure(board,n, 'usbMinusPin')    
    measure(board,n, 'usbPlusPin')    
    measure(board,n, 'firmware_test()')    
    measure(board,n, 'defines.__TIME__')    
    measure(board,n, 'pin("A0").an_in')    
    measure(board,n, 'reset()')    




  
