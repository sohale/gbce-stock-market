#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Utility functions for GBCE Simple Stock Market """

import datetime
import math
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

    SEC = 1000
    MIN = SEC * 60

    @staticmethod
    def numpy_time_now():
        return np.datetime64(datetime.datetime.now(), 'ms')

    @staticmethod
    def numpy_time_delta_min(minutes):
        assert TypeUtils.type_is_int(minutes)
        # return np.timedelta64(TimeUtils.MIN*minutes, 'ms')
        return TimeUtils.numpy_time_delta_msec(TimeUtils.MIN*minutes)

    @staticmethod
    def numpy_time_delta_msec(time_diff_ms):
        if math.fabs(math.floor(time_diff_ms) - time_diff_ms) > 0.000000001:
            raise Exception("time difference (delta) needs to be an integer, a factor of msec") 
        assert TypeUtils.type_is_int(time_diff_ms)
        return np.timedelta64(time_diff_ms, 'ms')


class CurrencyUtils(object):
    GBP_symbol = u"£".encode( "utf-8" )
    # u"P"

class TestUtils(object):
    @staticmethod
    def assertFloatEqual(testbject, arg1, arg2, tolerance=0.000001):
        """ a.k.a. assertAlmostEqual() """
        testbject.assertTrue( math.fabs(arg1 - arg2) < tolerance )

    @staticmethod
    def assertCurrencyEqual(testbject, arg1, arg2):
        raise Exception("Not implemented yet.")
