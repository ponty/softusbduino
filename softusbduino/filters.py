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
    values.sort()
    return 1.0 * sum(values) / filter_size


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
