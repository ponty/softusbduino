
from nose.tools import eq_
from softusbduino import filters


# def test_median():
#    def fread():
#        fread.x += 1
#        return [1, 2, 22][fread.x]
#    fread.x = -1
#    eq_(2, filters.median_filter(fread, 3))

def test_median():
    eq_(None, filters.median([]))
    eq_(0, filters.median([0]))
    eq_(1, filters.median([1]))
    eq_(1, filters.median([0, 1, 2]))
    eq_(1, filters.median([0, 1, 20]))


def test_average():
    eq_(None, filters.average([]))
    eq_(0, filters.average([0]))
    eq_(1, filters.average([1]))
    eq_(1, filters.average([0, 1, 2]))
    eq_(11, filters.average([0, 1, 2, 41]))
    eq_(1.5, filters.average([1, 2]))


def test_averaged_median():
#    eq_(None, filters.averaged_median([]))
#    eq_(0, filters.averaged_median([0]))
#    eq_(1, filters.averaged_median([1]))
#    eq_(1, filters.averaged_median([0,1,2]))
    eq_(1.5, filters.averaged_median([0, 1, 2, 3]))
    eq_(2, filters.averaged_median([0, 1, 2, 3, 4]))
