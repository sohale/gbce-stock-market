#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" GBCS Stock Demo """

import math
import numpy as np
import datetime

from trade import Trade



def example_100trades():
    """ Gnerates 100 random trades to experiment with."""
    all_trades = []


    for i in range(100):
        t = Trade(timestamp=np.datetime64(datetime.datetime.now(), 'ms'), \
            quantity=3+(i % 5), buysell_type=Trade.BUY, trade_price=1.00)
        t.invar()
        all_trades.append(t)
    print repr(all_trades)

    a1 = Trade.numpy_array(all_trades, False)
    a1rec = Trade.numpy_array(all_trades, True)
    assert a1.shape == (100,)
    assert a1rec.shape == (100,)

def get_recent_trades(time_diff_ms): #(from_ms, to_ms=0):
    """ Makes a collection of Trades in the given interval."""
    now_ms = np.datetime64(datetime.datetime.utcnow(), 'ms')
    from_ms = now_ms - time_diff_ms
    raise Exception("Not implemented "+str(from_ms)+" "+str(now_ms))

def demo_get15min():
    # Get trades in past 15 minute
    SEC = 1000
    MIN = SEC * 60
    #from_ms = now_ms - 15*MIN
    ts = get_recent_trades(15*MIN)
    print ">>ts<<", ts

# main: test
if __name__ == "__main__":

    demo_get15min()



# ===================================================================================

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
