#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import datetime

import datetime
import numpy as np

from trade import Trade


# In [14]: np.version.full_version
# Out[14]: '1.11.2'

def test1():
    """ Contains multiple unit test."""
    # Todo: should be in Pence (hundredth of a Pound, or in Pounds (GBP) with wo decimals)
    t = Trade(timestamp=np.datetime64('2005-02-25', 'ms'), quantity=13, buysell_type=Trade.BUY, trade_price=1.00);
    t.invar()
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

def example_100trades():
    all_trades = []


    for i in range(100):
        t = Trade(timestamp=np.datetime64(datetime.datetime.now(), 'ms'), quantity=13, buysell_type=Trade.BUY, trade_price=1.00);
        t.invar()
        all_trades.append(t)
    print repr(all_trades)

    a1 = Trade.numpy_array(all_trades, False)
    a1rec = Trade.numpy_array(all_trades, True)
    assert a1.shape == (100,)
    assert a1rec.shape == (100,)

def get_recent_trades(time_diff_ms): #(from_ms, to_ms=0):
    now_ms = np.datetime64(datetime.datetime.utcnow(), 'ms')
    from_ms = now_ms - time_diff_ms
    raise Exception("Not implemented")

def demo_get15min():
    # Get trades in past 15 minute
    SEC = 1000
    MIN = SEC * 60
    #from_ms = now_ms - 15*MIN
    ts = get_recent_trades(15*MIN)
    print ts

# main: test
if __name__ == "__main__":

    test1()
    demo_get15min()



# ===================================================================================

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


