#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" GBCS Stock Demo """

import numpy as np
import datetime

from trade import Trade
from gbce_utils import TimeUtils

class TradeSeries(object):
    """ An array of Trades, uses 'list' containting instances of a Trade class. """

    def __init__(self):
        """ Initialises an empty series """
        self.all_trades = []

    def add_example_100trades(self, count=10):
        """ Gnerates 100 random trades to experiment with."""

        for i in range(count):
            numpy_time_now =  TimeUtils.numpy_time_now()      # np.datetime64(datetime.datetime.now(), 'ms')
            ts = numpy_time_now - TimeUtils.numpy_time_delta_min(1)
            t = Trade(timestamp=ts, \
                quantity=3+(i % 5), buysell_type=Trade.BUY, trade_price=1.00)
            t.invar()
            self.all_trades.append(t)
        print repr(self.all_trades)

        #todo: refactor as a test
        a1 = self.get_numpy()
        assert a1.shape == (10,)

        #todo: refactor as a test
        a1rec = self.get_numpy_rec()
        assert a1rec.shape == (10,)

    def get_numpy(self):
        return Trade.numpy_array(self.all_trades, use_rec=False)

    def get_numpy_rec(self):
        return Trade.numpy_array(self.all_trades, use_rec=True)

    def _get_recent_trades(self, from_ms, to_ms):
        """ Selected a set of Trades in the given interval. Generator version. """
        for t in self.all_trades:
            if t.timestamp >= from_ms and t.timestamp < from_ms:
                yield t
    def get_recent_trades(self, time_diff_ms): #(from_ms, to_ms=0):
        """ Makes a collection of Trades in the given length of history. Generator version. """

        numpy_time_now_ms = TimeUtils.numpy_time_now() #np.datetime64(datetime.datetime.now(), 'ms')
        from_ms = numpy_time_now_ms - TimeUtils.numpy_time_delta_msec(time_diff_ms)
        #raise Exception("Not implemented "+str(from_ms)+" "+str(now_ms))
        return self._get_recent_trades(from_ms, numpy_time_now_ms)

def demo_get15min():
    # Get trades in past 15 minute
    ts1 = TradeSeries()
    ts1.add_example_100trades()
    #from_ms = now_ms - 15*TimeUtils.MIN
    ts2 = ts1.get_recent_trades(15*TimeUtils.MIN)
    print ">>ts<<", ts2

# main: test
if __name__ == "__main__":

    demo_get15min()



# ===================================================================================
import math

def checkmoney(x):
    # actual absolute money, not rate (e.g. price per share)
    # Makes sure the amount is in cents, not less
    assert abs(int(x*100)- (x*100)) < 0.000001

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


# ======End Points: calculate_*** methods ===============
"""
# Moved to class CompanyEntry:
def calculate_dividend_yield(market_price):
    return -1
"""
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
