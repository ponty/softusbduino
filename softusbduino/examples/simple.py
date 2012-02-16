from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino


@entrypoint
def main():
    board = Arduino()
    print board.defines.F_CPU
