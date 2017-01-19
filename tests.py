#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for various classes in GBCE, including Trade, CompanyEntry, Utils"""
import unittest2 as unittest
import numpy as np
from operator import xor

from trade import Trade
from company import CompanyEntry
from gbce_utils import TestUtils

# assert np.version.full_version >= '1.11.2'

class TradeTest(unittest.TestCase):
    """ Checks various things about instances of class Trade"""

    @staticmethod
    def example_trade():
        """ Generates a Trade objects, used in multiple tests. """
        # Todo: should be in Pence (hundredth of a Pound, or in Pounds (GBP) with wo decimals)
        trd = Trade(timestamp=np.datetime64('2005-02-25', 'ms'), \
            quantity=13, buysell_type=Trade.BUY, trade_price=1.00)
        trd.invar()
        return trd

    def test1(self):
        """ Contains multiple unit test."""
        trd = TradeTest.example_trade()
        print repr(trd.numpy())
        print repr(trd.numpy().shape)
        trd.invar()
        # print np.datetime64('2005-02-25')
        assert trd.timestamp - np.datetime64('2005-02-25', 'ms') == np.timedelta64(0, 'ms')
        assert trd.quantity == 13
        self.assertEqual(type(trd.quantity), int)

    def test_recoding_test(self):
        """ Re-coding means encoding and decoding back from and to another representation
           (here, numpy versus class)"""
        trd = TradeTest.example_trade()
        print repr(Trade.numpy_2_trade(trd.numpy()))
        recoded = Trade.numpy_2_trade(trd.numpy())
        print str(recoded)
        print recoded, trd, recoded == trd

        # Involves the timestamp's units
        self.assertEqual(trd, Trade.numpy_2_trade(trd.numpy()))  # used __eq__

    def assert_bad_trade_raises_exception(self, quantity, message_substring,\
            causes_exception=True):
        with self.assertRaises(Exception) as context:
            trd = Trade(timestamp=np.datetime64('2005-02-25', 'ms'), \
                quantity=quantity, buysell_type=Trade.BUY, trade_price=1.00)
            trd.invar()
        self.assertTrue(xor(message_substring in str(context.exception), \
            not bool(causes_exception)))

    def test_bad_trade(self):
        """ Tests whether non-int types are correctly detected """
        QUANTITY_INT_ERROR = 'Quantity has to be an integer'
        self.assert_bad_trade_raises_exception(13.01, QUANTITY_INT_ERROR)
        self.assert_bad_trade_raises_exception(13.00, QUANTITY_INT_ERROR)
        self.assert_bad_trade_raises_exception(0.00, QUANTITY_INT_ERROR)
        self.assert_bad_trade_raises_exception(0, QUANTITY_INT_ERROR, False)

class MiscTests(unittest.TestCase):
    """ Misc tests for versions, etc. """

    def tests_numpy_version(self):
        """
        >>> np.version.full_version
        '1.11.2'
        """
        self.assertTrue(np.version.full_version >= '1.11.2')

def some_doctests():
    """
    >>> 1
    1
    """
    return "OK"

class CompanyTest(unittest.TestCase):

    @staticmethod
    def example1():
        # GBCE
        t0 = CompanyEntry('TEA', CompanyEntry.CT.COMMON, 0, None, 100)
        t1 = CompanyEntry('POP', CompanyEntry.CT.COMMON, 8, None, 100)
        t2 = CompanyEntry('ALE', CompanyEntry.CT.COMMON, 23, None, 60)
        t3 = CompanyEntry('GIN', CompanyEntry.CT.PREFERRED, 8, 2, 100)
        t4 = CompanyEntry('JOE', CompanyEntry.CT.COMMON, 13, None, 250)
        print "Report based on market_value = 1.00 GBP for all comapnies:"
        tlist = [t0, t1, t2, t3, t4]
        return tlist

    def test_GBCE_company_etries(self):
        tlist = CompanyTest.example1()

        for t in tlist: print t.calculate_dividend_yield(1.0), t.report_company_info(1.0)

        # These numbers are not verified:
        TestUtils.assertFloatEqual(self, tlist[0].calculate_dividend_yield(1.0), 0.0)
        TestUtils.assertFloatEqual(self, tlist[1].calculate_dividend_yield(1.0), 8.0)
        TestUtils.assertFloatEqual(self, tlist[2].calculate_dividend_yield(1.0), 23)
        TestUtils.assertFloatEqual(self, tlist[3].calculate_dividend_yield(1.0), 2.0)
        TestUtils.assertFloatEqual(self, tlist[4].calculate_dividend_yield(1.0), 13.0)

from trade_series import TradeSeries
from gbce_utils import TimeUtils

class TradeSeriesTest(unittest.TestCase):
    @staticmethod
    def _add_example_100trades(testSelf, trade_series, count=100):
        """ Gnerates 100 random trades to experiment with."""

        for i in range(count):
            numpy_time_now = TimeUtils.numpy_time_now()
            OFFSET = -2  # To make sure it includes all of it, even depite being end-exlusive
            ts = numpy_time_now - TimeUtils.numpy_time_delta_min(1*i + OFFSET)
            trd = Trade(timestamp=ts, \
                quantity=3+(i % 5), buysell_type=Trade.BUY, trade_price=1.00)
            trd.invar()
            trade_series.all_trades.append(trd)
        # print repr(trade_series.all_trades) # large dump

        #todo: refactor as a test
        a1 = trade_series.get_numpy()
        testSelf.assertEqual(a1.shape, (count,))  # This is not the main purpose of the test though

        #todo: refactor as a test
        a1rec = trade_series.get_numpy_rec()
        testSelf.assertEqual(a1rec.shape, (count,))  # This is not the main purpose of the test though

    @staticmethod
    def select_15min(how_many_minutes, count, testSelf):
        # Gets trades in past 15 minute
        ts1 = TradeSeries()
        TradeSeriesTest._add_example_100trades(testSelf, ts1, count=count)
        ts1_recent_trades = ts1.select_recent_trades(how_many_minutes*TimeUtils.MIN)
        testSelf.assertEqual(len(ts1.all_trades), count)
        return ts1_recent_trades

    def test_select_15min(self):
        # Get trades in past 15 minute
        how_many_minutes = 15
        count = 100  # fixme: make sure this covers beyond number of minutes from both sides
        ts1_recent_trades = TradeSeriesTest.select_15min(how_many_minutes, count, self)

        selected_count = sum(1 for i in ts1_recent_trades)
        #for i in ts1.all_trades: print i, ;print
        #for i in ts1_recent_trades: print i, ;print
        self.assertEqual(selected_count, how_many_minutes)

    def test_volume_weighted_stock_price(self):
        how_many_minutes = 15
        count = 100  # fixme: make sure this covers beyond number of minutes from both sides
        selected_trades_iter = TradeSeriesTest.select_15min(how_many_minutes, count, self)
        vwsp =TradeSeries.calculate_volume_weighted_stock_price(selected_trades_iter)
        print "calculate_volume_weighted_stock_price: " , vwsp
        TestUtils.assertFloatEqual(self, vwsp, 1.0)  # 1.0 because all prices are 1.0, soany weighted average will be 1.0


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()
