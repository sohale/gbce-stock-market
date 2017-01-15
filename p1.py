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
       if not type(self.quantity) == int:
           print math.floor(self.quantity), self.quantity, math.floor(self.quantity) - self.quantity
           assert False, repr(self.quantity)
           print 
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
       return True

    def check(self):
        if not self.invar():
            raise Error("Invalid state")

    BIGBANG = np.datetime64(datetime.datetime(1800, 1, 1))

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
       return a1


# main: test
if __name__ == "__main__":
    pass

    # Todo: should be in Pence (hundredth of a Pound, or in Pounds (GBP) with wo decimals)
    t = Trade(timestamp=np.datetime64('2005-02-25'), quantity=1, buysell_type=Trade.BUY, trade_price=1.00);
    t.check()
    print repr(t.numpy())

    # (1,2.,'Hello'), (2,3.,"World")
    x = np.array([], \
      dtype=[('timestamp', np.datetime64),('quantity', 'i4'), ('buysell', 'b1'), ('price', 'f4')])  # todo: price will be fixed-point int
    # I keep the ints as signed to avoid accidental bugs, easire detection and tracing of of sign problems.



