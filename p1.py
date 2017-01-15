#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import datetime

# In [14]: np.version.full_version
# Out[14]: '1.11.2'


def checkmoney(x):
   # actual absolute money, not rate (e.g. price per share)
   # Makes sure the amount is in cents, not less
   assert(abs(int(x*100)- (x*100)) < 0.000001)

def fixmoney_floor(x):
   result = math.floor(x*100) * 0.0100000000
   checkmoney(result)
   return result

def fixmoney_ceil(x):
   result = math.ceil(x*100) * 0.0100000000
   checkmoney(result)
   return result

def fixmoney_round(x):
   result = math.round(x*100) * 0.0100000000
   checkmoney(result)
   return result


market_price = 1.00
shares = 4
paid = fixmoney_floor(market_price * shares)
#checkmoney(paid)

paid = fixmoney_floor(paid)
checkmoney(paid)


# =====================
def calculate_dividend_yield(market_price):
    return -1

def calculate_pe_ratio(market_price):
    return -1

def record_trade(self, timestamp, share_count, buy_notsell, trade_price):
    return -1

def calculate_Volume_Weighted_Stock_Price(self):
    return -1

# b. Calculate the GBCE All Share Index using the geometric mean of prices for all stocks
def calculate_GBCE(self):
    return -1

# dividend_yield = 

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
        assert self.invar()


    def invar(self):
       """ Invariant: checks validity of the object's state. """
       #print "**", self.timestamp - Trade.BIGBANG, " ----  ",  self.timestamp, " ----  ", Trade.BIGBANG
       if not self.timestamp > Trade.BIGBANG:
           assert False
           return False
       #if (math.floor(self.quantity)- self.quantity) == 0.0:
       if not( type(self.quantity) == int  or  type(self.quantity) == np.int32 ):
           print math.floor(self.quantity), self.quantity, math.floor(self.quantity) - self.quantity
           print type(self.quantity)  # numpy.int32
           assert False, repr(self.quantity)
           return False
       if not self.quantity > 0:
           assert False
           return False
       if not (self.buysell == Trade.BUY or self.buysell == Trade.SELL):
           assert False
           return False
       if not self.price > 0.0:
           assert False
           return False

       # Make sure the units are in milliseconds
       if not str(self.timestamp.dtype) == 'datetime64[ms]':
           assert False, "Timesctap units must me milliseconds"
           return False

       if not repr(self.timestamp.dtype) == "dtype('<M8[ms]')":
           assert False, "Timesctap units must me milliseconds"
           return False

       # recoding test is done in unittests

       return True

    def check(self):
        if not self.invar():
            raise Error("Invalid state")

    BIGBANG = np.datetime64(datetime.datetime(1800, 1, 1), 'ms')

    EXAMPLE1 = np.array([(datetime.datetime(1800, 1, 1), 2, SELL, 1.0)], \
      dtype=[('timestamp', 'datetime64[ms]'),('quantity', 'i4'), ('buysell', 'b1'), ('price', 'f4')])

    EMPTY = np.array([], \
      dtype=[('timestamp', 'datetime64[ms]'),('quantity', 'i4'), ('buysell', 'b1'), ('price', 'f4')])

    # An array for each field
    #EMPTY_REC = np.rec.array([], \
    #  dtype=[('timestamp', 'datetime64[ms]'),('quantity', 'i4'), ('buysell', 'b1'), ('price', 'f4')])

    #
    # h	hour	+/- 1.0e15 years	[1.0e15 BC, 1.0e15 AD]
    # m	minute	+/- 1.7e13 years	[1.7e13 BC, 1.7e13 AD]
    # s	second	+/- 2.9e12 years	[ 2.9e9 BC, 2.9e9 AD]
    # ms	millisecond	+/- 2.9e9 years	[ 2.9e6 BC, 2.9e6 AD]
    # us	microsecond	+/- 2.9e6 years	[290301 BC, 294241 AD]
    # ns	nanosecond	+/- 292 years	[ 1678 AD, 2262 AD]

    def numpy(self):
       a1 = np.array([(self.timestamp, self.quantity, self.buysell, self.price)], \
          dtype=[('timestamp', 'datetime64[ms]'),('quantity', 'i4'), ('buysell', 'b1'), ('price', 'f4')])
       # I keep the ints as signed to avoid accidental bugs, easire detection and tracing of of sign problems.
       # todo: price will be fixed-point int
       return a1

    @staticmethod
    def numpy_2_trade(a):
        assert a.shape == (1,)
        obj = Trade(a[0]['timestamp'], a[0]['quantity'], a[0]['buysell'], a[0]['price'])
        assert obj.invar()
        return obj

    def currency_symbol(self):
        return u"£".encode( "utf-8" )

    def __repr__(self):
       return "Trade:"+str(self.quantity)+"x" +self.currency_symbol()+str(self.price)+":"+('BUY' if self.buysell==Trade.BUY else 'SELL')+"@"+str(self.timestamp)

    def __eq__(self, other):
       return self.quantity == other.quantity    \
          and self.price == other.price          \
          and self.buysell == other.buysell      \
          and self.timestamp == other.timestamp


def test1():
    """ Contains multiple unit test."""
    # Todo: should be in Pence (hundredth of a Pound, or in Pounds (GBP) with wo decimals)
    t = Trade(timestamp=np.datetime64('2005-02-25', 'ms'), quantity=13, buysell_type=Trade.BUY, trade_price=1.00);
    t.check()
    print repr(t.numpy())
    print repr(t.numpy().shape)
    assert t.invar()
    #print np.datetime64('2005-02-25')
    assert t.timestamp - np.datetime64('2005-02-25','ms')  == np.timedelta64(0,'ms')
    assert t.quantity == 13
    assert type(t.quantity) == int
    print repr(Trade.numpy_2_trade(t.numpy()))
    recoded = Trade.numpy_2_trade(t.numpy())
    print str(recoded)
    print recoded, t, recoded == t

    assert t == Trade.numpy_2_trade(t.numpy())  # timestamp's units


# main: test
if __name__ == "__main__":

    test1()

