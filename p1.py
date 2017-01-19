#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" GBCS Stock Demo """

#from trade import Trade
#from gbce_utils import TimeUtils


def demo_get15min():
    pass

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
