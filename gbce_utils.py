""" Utility functions for GBCE Simple Stock Market """

import datetime
import numpy as np

class TypeUtils(object):
    """ A static class that is simply a collection of static functions. """

    @staticmethod
    def type_is_int(value):
        """ Checks if a value is of an int type. Is used in check() and other class invariants."""
        # return type(value) is int  or  type(value) == np.int32
        return isinstance(value, int)  or  isinstance(value, np.int32)

class TimeUtils(object):

    ############## Timestamp utils ############

    # """ The origin of time. """
    BIGBANG = np.datetime64(datetime.datetime(1800, 1, 1), 'ms')

    #
    # h	hour	+/- 1.0e15 years	[1.0e15 BC, 1.0e15 AD]
    # m	minute	+/- 1.7e13 years	[1.7e13 BC, 1.7e13 AD]
    # s	second	+/- 2.9e12 years	[ 2.9e9 BC, 2.9e9 AD]
    # ms	millisecond	+/- 2.9e9 years	[ 2.9e6 BC, 2.9e6 AD]
    # us	microsecond	+/- 2.9e6 years	[290301 BC, 294241 AD]
    # ns	nanosecond	+/- 292 years	[ 1678 AD, 2262 AD]
