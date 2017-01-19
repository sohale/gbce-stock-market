#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for various classes in GBCE, including Trade, CompanyEntry, Utils"""
import unittest2 as unittest
import numpy as np
from operator import xor

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
        """ Re-coding means encoding and decoding back from and to another representation (here, numpy versus class)"""
        t = TradeTest.example_trade()
        print repr(Trade.numpy_2_trade(t.numpy()))
        recoded = Trade.numpy_2_trade(t.numpy())
        print str(recoded)
        print recoded, t, recoded == t

        assert t == Trade.numpy_2_trade(t.numpy())  # timestamp's units

    def _assert_bad_trade_raises_exception(self, quantity, message_substring, causes_exception=True):
        with self.assertRaises(Exception) as context:
            t = Trade(timestamp=np.datetime64('2005-02-25', 'ms'), quantity=quantity, buysell_type=Trade.BUY, trade_price=1.00)
            t.invar()
        self.assertTrue(xor(message_substring in str(context.exception), not bool(causes_exception)))

    def test_bad_trade(self):
        """ Tests whether non-int types are correctly detected """
        self._assert_bad_trade_raises_exception(13.01, 'Quantity has to be an integer')
        self._assert_bad_trade_raises_exception(13.00, 'Quantity has to be an integer')
        self._assert_bad_trade_raises_exception(0.00, 'Quantity has to be an integer')
        self._assert_bad_trade_raises_exception(0, 'Quantity has to be an integer', False)

class MiscTests(unittest.TestCase):
    def tests_numpy_version(self):
        # In [14]: np.version.full_version
        # Out[14]: '1.11.2'
        self.assertTrue(np.version.full_version >= '1.11.2')

def some_doctests():
    return "OK"

class CompanyTest(unittest.TestCase):
    def test_GBCE_company_etries(self):
        # GBCE
        t1 = CompanyEntry('TEA', CompanyEntry.CT.COMMON, 0, None, 100)
        t2 = CompanyEntry('POP', CompanyEntry.CT.COMMON, 8, None, 100)
        t3 = CompanyEntry('ALE', CompanyEntry.CT.COMMON, 23, None, 60)
        t4 = CompanyEntry('GIN', CompanyEntry.CT.PREFERRED, 8, 2, 100)
        t5 = CompanyEntry('JOE', CompanyEntry.CT.COMMON, 13, None, 250)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()

