#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" GBCS Stock Demo """

def demo_get15min():
    print 'Please run "python tests.py" instead'

if __name__ == "__main__":
    demo_get15min()



# ===================================================================================

def checkmoney(x):
    """
    Used for an actual absolute amount of money, not rate or price per share, etc
    Makes sure the amount is in cents, i.e. has two decimals, and not a fraction of a Cent/Pence.
    """
    assert abs(int(x*100)- (x*100)) < 0.0000001

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
