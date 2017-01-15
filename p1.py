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

from trade import Trade

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

