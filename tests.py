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
        t = TradeTest.example_trade()
        print repr(t.numpy())
        print repr(t.numpy().shape)
        t.invar()
        # print np.datetime64('2005-02-25')
        assert t.timestamp - np.datetime64('2005-02-25', 'ms') == np.timedelta64(0, 'ms')
        assert t.quantity == 13
        self.assertEqual(type(t.quantity), int)

    def test_recoding_test(self):
        """ Re-coding means encoding and decoding back from and to another representation
           (here, numpy versus class)"""
        t = TradeTest.example_trade()
        print repr(Trade.numpy_2_trade(t.numpy()))
        recoded = Trade.numpy_2_trade(t.numpy())
        print str(recoded)
        print recoded, t, recoded == t

        # Involves the timestamp's units
        assert t == Trade.numpy_2_trade(t.numpy())

    def _assert_bad_trade_raises_exception(self, quantity, message_substring,\
            causes_exception=True):
        with self.assertRaises(Exception) as context:
            t = Trade( timestamp=np.datetime64('2005-02-25', 'ms'), \
                quantity=quantity, buysell_type=Trade.BUY, trade_price=1.00)
            t.invar()
        self.assertTrue(xor(message_substring in str(context.exception), \
            not bool(causes_exception)))

    def test_bad_trade(self):
        """ Tests whether non-int types are correctly detected """
        QUANTITY_INT_ERROR = 'Quantity has to be an integer'
        self._assert_bad_trade_raises_exception(13.01, QUANTITY_INT_ERROR)
        self._assert_bad_trade_raises_exception(13.00, QUANTITY_INT_ERROR)
        self._assert_bad_trade_raises_exception(0.00, QUANTITY_INT_ERROR)
        self._assert_bad_trade_raises_exception(0, QUANTITY_INT_ERROR, False)

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
        self.assertEqual( t1.calculate_dividend_yield(1.0), 0)

from trade_series import TradeSeries
from gbce_utils import TimeUtils

class TradeSeriesTest(unittest.TestCase):
    @staticmethod
    def _add_example_100trades(trade_series, count=100):
        """ Gnerates 100 random trades to experiment with."""

        for i in range(count):
            numpy_time_now =  TimeUtils.numpy_time_now()      # np.datetime64(datetime.datetime.now(), 'ms')
            OFFSET = -2  # To make sure it includes all of it, even depite being end-exlusive
            ts = numpy_time_now - TimeUtils.numpy_time_delta_min( 1*i + OFFSET)
            t = Trade(timestamp=ts, \
                quantity=3+(i % 5), buysell_type=Trade.BUY, trade_price=1.00)
            t.invar()
            trade_series.all_trades.append(t)
        print repr(trade_series.all_trades)

        #todo: refactor as a test
        a1 = trade_series.get_numpy()
        assert a1.shape == (count,)

        #todo: refactor as a test
        a1rec = trade_series.get_numpy_rec()
        assert a1rec.shape == (count,)

    def test_get15min(self):
        # Get trades in past 15 minute
        ts1 = TradeSeries()
        how_many_minutes = 15
        count = 100  # fixme: make sure this covers beyond number of minutes from both sides
        TradeSeriesTest._add_example_100trades(ts1, count=count)
        ts1_recent_trades = ts1.select_recent_trades(how_many_minutes*TimeUtils.MIN)
        selected_count = sum(1 for i in ts1_recent_trades)
        #for i in ts1.all_trades: print i, ;print
        #for i in ts1_recent_trades: print i, ;print
        self.assertEqual(len(ts1.all_trades), count)
        self.assertEqual( selected_count, how_many_minutes)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()
