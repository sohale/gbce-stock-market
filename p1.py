#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" GBCS Stock Demo """

def demo_get15min():
    print 'Please run "python tests.py" instead'

if __name__ == "__main__":
    demo_get15min()



# ===================================================================================

from gbce_utils import CurrencyUtils

def test_currencyUtils():
    market_price = 1.00
    shares = 4
    paid = CurrencyUtils.fixmoney_floor(market_price * shares)
    #CurrencyUtils.checkmoney(paid)

    paid = CurrencyUtils.fixmoney_floor(paid)
    CurrencyUtils.checkmoney(paid)

test_currencyUtils()
