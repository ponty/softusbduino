from __future__ import division
from decotrace import traced
import time


def median(ls):
    '''
    median filter
    '''
    if not len(ls):
        return
    values = list(ls)
    values.sort()
    return values[int(len(values) / 2)]


def average(ls):
    if not len(ls):
        return
    return sum(ls) / len(ls)


def averaged_median(ls, median_window=3):
    if not len(ls):
        return
    if len(ls) <= median_window:
        return median(ls)
    ls2 = []
    for i in range(len(ls) - median_window + 1):
        ls2 += [median(ls[i:i + median_window])]
    return average(ls2)


def read_analog_list(pin, count, delay=0.001):
    ls = []
    for _ in range(count):
        x = pin.read_analog()
        time.sleep(delay)
        ls += [x]
    return ls


def filtered_analog(pin, median_window=3, average_window=20):
    ls = [median(
        read_analog_list(pin, median_window)) for _ in range(average_window)]
    return    average(ls)


def median_filter(fread, filter_size):
    '''
    median filter
    '''
    values = [fread() for _ in range(filter_size)]
    values.sort()
    return values[int(filter_size / 2)]


def average_filter(fread, filter_size):
    '''
    '''
    values = [fread() for _ in range(filter_size)]
    return sum(values) / filter_size


def same_filter(fread, filter_size):
    same_count = 0
    v = None
    while same_count < filter_size:
        val_last = fread()
        if val_last == v:
            same_count += 1
        else:
            same_count = 0
            v = val_last
