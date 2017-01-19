#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from company import CompanyEntry
from gbce_utils import TypeUtils
from gbce_utils import TimeUtils
from gbce_utils import CurrencyUtils

class Trade(object):
    """ A Trade, of the stock of a specific company, with a specific price. """

    BUY = True
    SELL = False

    def __init__(self, company_obj, timestamp, quantity, buysell_type, trade_price):
        """
        @param company_obj: is not Nullable (not None).
        @param quantity: Quantity (number) of shares: Integer >= 1
        @param price: Trade price. price > 0
        """
        self.company_obj = company_obj
        #if self.company_obj is not None:
        self.company_obj.check()
        self.timestamp = timestamp
        self.quantity = quantity
        self.buysell = buysell_type
        self.price = trade_price
        self.check()

    def check(self):
        """ Class Invariant: checks (asserts) consistency (validity) of the object's state. """

        if not isinstance(self.company_obj, CompanyEntry):
            raise Exception("Company object is not provided.")

        if not self.timestamp > TimeUtils.BIGBANG:
            raise Exception("timestamp went wrong")

        if not TypeUtils.type_is_int(self.quantity):
            raise Exception("Quantity has to be an integer: " + repr(self.quantity)+ " type="+str(type(self.quantity)))

        if not self.quantity > 0:
            raise Exception("Quantity has to be a positive number")

        if not (self.buysell == Trade.BUY or self.buysell == Trade.SELL):
            raise Exception("Trade type has to be either Trade.BUY or Trade.SELL: "+repr(self.buysell)+" Has to be in "+str([Trade.BUY,Trade.SELL]))

        if not self.price > 0.0:
            # math.log(self.price) is meaningful
            raise Exception("Trade price has to be a real positive number")

        # Make sure the units are in milliseconds
        if not str(self.timestamp.dtype) == 'datetime64[ms]':
            raise Exception("Timestamo units must me milliseconds."+str(self.timestamp.dtype))
 
        if not repr(self.timestamp.dtype) == "dtype('<M8[ms]')":
            raise Exception("Timestamo units must me milliseconds."+repr(self.timestamp.dtype))

        # The "recoding" test is done in tests.py
        #enable usage `assert x.check`, which ignores this in `python -O3` optimised mode
        return True

    # todo: use int for abbrev for faster selecting of the targte company on the numpy array
    numpy_dtype = [('timestamp', 'datetime64[ms]'),('quantity', 'i4'), ('buysell', 'b1'), ('price', 'f4'), ('abbrev', 'S3')]

    EXAMPLE1 = np.array([(TimeUtils.BIGBANG, 2, SELL, 1.0, 'ABC')], \
      dtype=numpy_dtype)

    EMPTY = np.array([], numpy_dtype)

    # An array for each field
    #EMPTY_REC = np.rec.array([], \
    #  dtype=numpy_dtype)


    def numpy(self):
        #todo: @param: relative time difference reference
        a1 = np.array([ self.to_tuple() ], \
          dtype=Trade.numpy_dtype )
        # I keep the ints as signed to avoid accidental bugs, easire detection and tracing of of sign problems.
        # todo: price will be fixed-point int
        return a1

    @staticmethod
    def numpy_array(list_of_trades, use_rec):
        l = []
        for t in list_of_trades:
            assert t.check()
            l.append(t.to_tuple())

        if not use_rec:
            return np.array(l, dtype=Trade.numpy_dtype )
        else:
            # Not tested
            return np.rec.array(l, dtype=Trade.numpy_dtype )

    def to_tuple(self):
        abbrv = self.company_obj.abbrev
        assert len(abbrv) == 3
        return (self.timestamp, self.quantity, self.buysell, self.price, abbrv)

    # For _numpy_2_trade() see Market

    def currency_symbol(self):
        return CurrencyUtils.GBP_symbol

    def __repr__(self):
        """Return the square of x.

        >>> t = Trade(None, timestamp=np.datetime64('2005-02-25', 'ms'), quantity=13, buysell_type=Trade.BUY, trade_price=1.00); repr(t)
        'T rade:13xP1.0:BUY@2005-02-25T00:00:00.000'
        """

        return "Trade:"+(self.company_obj.abbrev)+";("+('BUY' if self.buysell==Trade.BUY else 'SELL')+")"+str(self.quantity)+"x" +self.currency_symbol()+str(self.price)+"@"+str(self.timestamp)

    def __eq__(self, other):
        return self.quantity == other.quantity    \
          and self.price == other.price          \
          and self.buysell == other.buysell      \
          and self.timestamp == other.timestamp

if __name__ == '__main__':
    import doctest
    doctest.testmod()
