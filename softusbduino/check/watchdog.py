from entrypoint2 import entrypoint
from softusbduino.arduino import Arduino
import logging
import time

log = logging


@entrypoint
def main(
    timeout=2,
    sleep=1,
):
    mcu = Arduino(auto_reconnect=False)
    mcu.watchdog.start(timeout)
    time.sleep(sleep)
    mcu.watchdog.stop()
#    time.sleep(3)
