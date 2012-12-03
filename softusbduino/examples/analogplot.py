from entrypoint2 import entrypoint
from matplotlib.ticker import FuncFormatter
from softusbduino.arduino import Arduino
import matplotlib.pyplot as plt
import time


@entrypoint
def main(n=40, pin_nr=13, reset=False):
    '''
    measuring analog input
    '''
    mcu = Arduino(reset=reset)
    pin = mcu.pin(pin_nr)

    x = []
    y = []
    start = time.time()
    for i in range(n):
        t = time.time() - start
        v = pin.read_analog()
        x.append(t)
        y.append(v)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y, 'b-o')

    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%d') % (x)))
    ax.set_ylabel('analog value')

    ax.xaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: '%.0f' % (1000 * x)))
    ax.set_xlabel('milliseconds')
    plt.show()
