#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import datetime
import datetime
import numpy as np

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
       #print "**", self.timestamp - Trade.BIGBANG, " ----  ",  self.timestamp, " ----  ", Trade.BIGBANG
       if not self.timestamp > Trade.BIGBANG:
           raise Exception("timestamp went wrong")
       #if (math.floor(self.quantity)- self.quantity) == 0.0:
       if not( type(self.quantity) == int  or  type(self.quantity) == np.int32 ):
           #print math.floor(self.quantity), self.quantity, math.floor(self.quantity) - self.quantity
           #print type(self.quantity)  # numpy.int32
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

    BIGBANG = np.datetime64(datetime.datetime(1800, 1, 1), 'ms')

    EXAMPLE1 = np.array([(datetime.datetime(1800, 1, 1), 2, SELL, 1.0)], \
      dtype=numpy_dtype)

    EMPTY = np.array([], numpy_dtype)

    # An array for each field
    #EMPTY_REC = np.rec.array([], \
    #  dtype=numpy_dtype)

    #
    # h	hour	+/- 1.0e15 years	[1.0e15 BC, 1.0e15 AD]
    # m	minute	+/- 1.7e13 years	[1.7e13 BC, 1.7e13 AD]
    # s	second	+/- 2.9e12 years	[ 2.9e9 BC, 2.9e9 AD]
    # ms	millisecond	+/- 2.9e9 years	[ 2.9e6 BC, 2.9e6 AD]
    # us	microsecond	+/- 2.9e6 years	[290301 BC, 294241 AD]
    # ns	nanosecond	+/- 292 years	[ 1678 AD, 2262 AD]

    def numpy(self):
       #todo: @param: relative time difference reference
       a1 = np.array([(self.timestamp, self.quantity, self.buysell, self.price)], \
          dtype=Trade.numpy_dtype )
       # I keep the ints as signed to avoid accidental bugs, easire detection and tracing of of sign problems.
       # todo: price will be fixed-point int
       return a1

    @staticmethod
    def numpy_array(list_of_trades,use_rec):
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


