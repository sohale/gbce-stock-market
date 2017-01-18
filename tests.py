#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2 as unittest
import numpy as np

from trade import Trade
from company import CompanyEntry

# assert np.version.full_version >= '1.11.2'

class TradeTest(unittest.TestCase):

    @staticmethod
    def example_trade():
        # Todo: should be in Pence (hundredth of a Pound, or in Pounds (GBP) with wo decimals)
        t = Trade(timestamp=np.datetime64('2005-02-25', 'ms'), quantity=13, buysell_type=Trade.BUY, trade_price=1.00)
        t.invar()
        return t

    def test1(self):
        """ Contains multiple unit test."""
        t = TradeTest.example_trade()
        print repr(t.numpy())
        print repr(t.numpy().shape)
        t.invar()
        #print np.datetime64('2005-02-25')
        assert t.timestamp - np.datetime64('2005-02-25','ms')  == np.timedelta64(0,'ms')
        assert t.quantity == 13
        assert type(t.quantity) == int

    def test_recoding_test(self):
        t = TradeTest.example_trade()
        print repr(Trade.numpy_2_trade(t.numpy()))
        recoded = Trade.numpy_2_trade(t.numpy())
        print str(recoded)
        print recoded, t, recoded == t

        assert t == Trade.numpy_2_trade(t.numpy())  # timestamp's units

def some_doctests():
    return "OK"

class CompanyTest(unittest.TestCase):
    def test_GBCE_company_etries(self):
        # GBCE
        t = CompanyEntry('TEA', CompanyEntry.CT.COMMON, 0, None, 100)
        t = CompanyEntry('POP', CompanyEntry.CT.COMMON, 8, None, 100)
        t = CompanyEntry('ALE', CompanyEntry.CT.COMMON, 23, None, 60)
        t = CompanyEntry('GIN', CompanyEntry.CT.PREFERRED, 8, 2, 100)
        t = CompanyEntry('JOE', CompanyEntry.CT.COMMON, 13, None, 250)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()

