#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import datetime

from gbce_utils import TypeUtils
from gbce_utils import TimeUtils

class Trade(object):

    BUY = True
    SELL = False

    def __init__(self, timestamp, quantity, buysell_type, trade_price):
        self.timestamp = timestamp
        "Quantity (number) of shares: Integer >= 1"
        self.quantity = quantity
        self.buysell = buysell_type
        "Trade price. price > 0"
        self.price = trade_price
        self.invar()


    def invar(self):
        """ Class Invariant: checks (asserts) consistency (validity) of the object's state. """
        if not self.timestamp > TimeUtils.BIGBANG:
            raise Exception("timestamp went wrong")

        if not TypeUtils.type_is_int(self.quantity):
            raise Exception("Quantity has to be an integer: " + repr(self.quantity)+ " type="+str(type(self.quantity)))

        if not self.quantity > 0:
            raise Exception("Quantity has to be a positive number")

        if not (self.buysell == Trade.BUY or self.buysell == Trade.SELL):
            raise Exception("Trade type has to be either Trade.BUY or Trade.SELL: "+repr(self.buysell)+" Has to be in "+str([Trade.BUY,Trade.SELL]))

        if not self.price > 0.0:
            raise Exception("Trade price has to be a real positive number")

        # Make sure the units are in milliseconds
        if not str(self.timestamp.dtype) == 'datetime64[ms]':
            raise Exception("Timestamo units must me milliseconds."+str(self.timestamp.dtype))
 
        if not repr(self.timestamp.dtype) == "dtype('<M8[ms]')":
            raise Exception("Timestamo units must me milliseconds."+repr(self.timestamp.dtype))

        # The "recoding" test is done in tests.py
        #enable usage `assert x.invar`, which ignores this in `python -O3` optimised mode
        return True


    numpy_dtype = [('timestamp', 'datetime64[ms]'),('quantity', 'i4'), ('buysell', 'b1'), ('price', 'f4')]

    EXAMPLE1 = np.array([(TimeUtils.BIGBANG, 2, SELL, 1.0)], \
      dtype=numpy_dtype)

    EMPTY = np.array([], numpy_dtype)

    # An array for each field
    #EMPTY_REC = np.rec.array([], \
    #  dtype=numpy_dtype)


    def numpy(self):
        #todo: @param: relative time difference reference
        a1 = np.array([(self.timestamp, self.quantity, self.buysell, self.price)], \
          dtype=Trade.numpy_dtype )
        # I keep the ints as signed to avoid accidental bugs, easire detection and tracing of of sign problems.
        # todo: price will be fixed-point int
        return a1

    @staticmethod
    def numpy_array(list_of_trades, use_rec):
        l = []
        for t in list_of_trades:
            assert t.invar()
            l.append(t.to_tuple())

        if not use_rec:
            return np.array(l, dtype=Trade.numpy_dtype )
        else:
            # Not tested
            return np.rec.array(l, dtype=Trade.numpy_dtype )

    def to_tuple(self):
        return (self.timestamp, self.quantity, self.buysell, self.price)


    @staticmethod
    def numpy_2_trade(a):
        assert a.shape == (1,)
        obj = Trade(a[0]['timestamp'], a[0]['quantity'], a[0]['buysell'], a[0]['price'])
        obj.invar()
        return obj

    def currency_symbol(self):
        # return u"£".encode( "utf-8" )
        return u"P"

    def __repr__(self):
        """Return the square of x.

        >>> t = Trade(timestamp=np.datetime64('2005-02-25', 'ms'), quantity=13, buysell_type=Trade.BUY, trade_price=1.00); repr(t)
        'Trade:13xP1.0:BU Y@2005-02-25T00:00:00.000'
        """

        return "Trade:"+str(self.quantity)+"x" +self.currency_symbol()+str(self.price)+":"+('BUY' if self.buysell==Trade.BUY else 'SELL')+"@"+str(self.timestamp)

    def __eq__(self, other):
        return self.quantity == other.quantity    \
          and self.price == other.price          \
          and self.buysell == other.buysell      \
          and self.timestamp == other.timestamp


