#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for various classes in GBCE, including Trade, CompanyEntry, Utils"""
import unittest2 as unittest
import numpy as np
from operator import xor

from trade import Trade
from company import CompanyEntry
from gbce_utils import TestUtils
from gbce_utils import CurrencyUtils

from market import Market
from numpy_trades import NumpyTrades

class TradeTest(unittest.TestCase):
    """ Checks various things about instances of class Trade"""

    @staticmethod
    def example_trade():
        """ Generates a Trade objects, used in multiple tests. """
        # Todo: should be in Pence (hundredth of a Pound, or in Pounds (GBP) with wo decimals)
        c = CompanyTest.example_company2()
        trd = Trade(c, timestamp=np.datetime64('2005-02-25', 'ms'), \
            quantity=13, buysell_type=Trade.BUY, trade_price=1.00)
        trd.check()
        companies_list = { c.abbrev: c }  # !
        return trd, companies_list

    def test_1(self):
        """ Contains multiple unit test."""
        trd, companies_list = TradeTest.example_trade()
        # print repr(trd.numpy())
        self.assertEqual(trd.numpy().shape, (1,))
        trd.check()
        # print np.datetime64('2005-02-25')
        self.assertEqual(trd.timestamp - np.datetime64('2005-02-25', 'ms'), np.timedelta64(0, 'ms') )
        self.assertEqual(trd.quantity, 13)
        self.assertEqual(type(trd.quantity), int)

    def test_recoding_test(self):
        """ Re-coding means encoding and decoding back from and to another representation
           (here, numpy versus class)"""
        trd, companies_list = TradeTest.example_trade()
        decoded_trades_list = Market._numpy_2_trade(trd.numpy(), companies_list)
        self.assertEqual(len(decoded_trades_list), 1 )
        # print repr(decoded_trades_list[0])
        recoded = decoded_trades_list[0]
        # print "**************", str(recoded)
        # print recoded, trd, recoded == trd
        self.assertEqual(recoded, trd)

        # Involves the timestamp's units
        self.assertEqual(trd, decoded_trades_list[0])  # used __eq__

    def assert_bad_trade_raises_exception(self, quantity, message_substring,\
            causes_exception=True):
        company_obj = CompanyTest.example_company2()
        with self.assertRaises(Exception) as context:
            trd = Trade(company_obj, timestamp=np.datetime64('2005-02-25', 'ms'), \
                quantity=quantity, buysell_type=Trade.BUY, trade_price=1.00)
            trd.check()
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

    @staticmethod
    def example_company1():
        return CompanyEntry('TEA', CompanyEntry.CT.COMMON, 0, None, 100)

    @staticmethod
    def example_company2():
        return CompanyEntry('GIN', CompanyEntry.CT.PREFERRED, 8, 2, 100)

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
    def _generate_example_100trades(testSelf, trade_series, count=100, randomise_mixed_companies=False):
        """ Gnerates 100 random trades to experiment with."""

        c2 = CompanyTest.example_company2()
        c1 = CompanyTest.example_company1()
        for i in range(count):
            numpy_time_now = TimeUtils.numpy_time_now()
            OFFSET = -2  # To make sure it includes all of it, even depite being end-exlusive
            ts = numpy_time_now - TimeUtils.numpy_time_delta_min(1*i + OFFSET)
            if randomise_mixed_companies:
                c = c1 if np.random.rand() < 0.7 else c2
            else:
                c = c2
            trd = Trade(c, timestamp=ts, \
                quantity=3+(i % 5), buysell_type=Trade.BUY, trade_price=1.00)
            trd.check()
            trade_series.all_trades.append(trd)
        # print repr(trade_series.all_trades) # large dump

        #todo: refactor as a test
        a1 = trade_series.get_numpy()
        testSelf.assertEqual(a1.shape, (count,))  # This is not the main purpose of the test though

        #todo: refactor as a test
        a1rec = trade_series.get_numpy_rec()
        testSelf.assertEqual(a1rec.shape, (count,))  # This is not the main purpose of the test though

    @staticmethod
    def generate_and_select_15min(how_many_minutes, count, testSelf, company_code):
        """
        @param company_code: company_code can be None, in that case
        """
        # Gets trades in past 15 minute
        ts1 = TradeSeries()
        TradeSeriesTest._generate_example_100trades(testSelf, ts1, count=count)
        ts1_recent_trades = ts1.select_recent_trades(how_many_minutes*TimeUtils.MIN, company_code=company_code)
        testSelf.assertEqual(len(ts1.all_trades), count)
        return ts1_recent_trades

    def test_select_15min(self):
        # Get trades in past 15 minute
        company_code = None
        how_many_minutes = 15
        count = 100  # fixme: make sure this covers beyond number of minutes from both sides
        ts1_recent_trades = TradeSeriesTest.generate_and_select_15min(how_many_minutes, count, self, company_code=company_code)

        selected_count = sum(1 for i in ts1_recent_trades)
        #for i in ts1.all_trades: print i, ;print
        #for i in ts1_recent_trades: print i, ;print
        self.assertEqual(selected_count, how_many_minutes)

    def test_volume_weighted_stock_price(self):
        company_code = 'GIN' #'TEA'  # None  # must be a specific company
        how_many_minutes = 15
        count = 100  # fixme: make sure this covers beyond number of minutes from both sides
        print "Volume Weighted Stock Price: ",
        selected_trades_iter = TradeSeriesTest.generate_and_select_15min(how_many_minutes, count, self, company_code=company_code)
        vwsp =TradeSeries.calculate_volume_weighted_stock_price(selected_trades_iter)
        print "Volume Weighted Stock Price: ", vwsp
        TestUtils.assertFloatEqual(self, vwsp, 1.0)  # 1.0 because all prices are 1.0, soany weighted average will be 1.0

    def test_GBCE_AllShare_Index(self):
        """
        Calculate the GBCE All-Share Index using the geometric mean of prices for all stocks
        """
        how_many_minutes = 15
        count = 100  # fixme: make sure this covers beyond number of minutes from both sides
        print "All-Share Index: ",
        selected_trades_iter = TradeSeriesTest.generate_and_select_15min(how_many_minutes, count, self, None)   # all companies
        asi = TradeSeries.calculate_geometric_mean(selected_trades_iter)
        print "All-Share Index: ", asi
        TestUtils.assertFloatEqual(self, asi, 1.0)


class CurrencyUtilsTest(unittest.TestCase):

    def test_currencyUtils(self):
        market_price = 1.00
        shares = 4
        paid = CurrencyUtils.fixmoney_floor(market_price * shares)
        #CurrencyUtils.checkmoney(paid)

        paid = CurrencyUtils.fixmoney_floor(paid)
        CurrencyUtils.checkmoney(paid)

class MarketTest(unittest.TestCase):

    def test_market_numpy1_select_then_numpy(self):
        """ First selects the trades using a selector, then convertsinto a numpy array representation.

        Filtering can be done either before (here) or after (*1) conversion into numpy.
        *1 : See `test_market_numpy2_mixed()`
        """
        count = 100
        selected_company_code = 'GIN'
        how_many_minutes = 1500
        market = Market()
        TradeSeriesTest._generate_example_100trades(self, market.trade_series, count=count, randomise_mixed_companies=True)
        trades_iterable = market.trade_series.select_recent_trades(how_many_minutes*TimeUtils.MIN, company_code=selected_company_code)
        n = market.make_numpy(trades_iterable)
        # print "big numpy shape: ", n.shape  # typical result: (31,)

    def test_market_numpy2_mixed(self):
        """ First converts the whole market into a numpy array representation,
        then selects using numpy. Fast operations: Suitable for operations on
        large numbers of trades.
        
        Filtering can be done either before (*2) or after (here) conversion into numpy.
        *2: See `test_market_numpy1_select_then_numpy()`
        """
        count = 1000

        market = Market()
        TradeSeriesTest._generate_example_100trades(self, market.trade_series, 
            count=count, randomise_mixed_companies=True)
        trades_iterable = market.trade_series.select_all_trades()
        n = market.make_numpy(trades_iterable)
        self.assertEqual(n.shape, (count,))
        # print "big numpy shape: ", n.shape
        # print n

        # Exmaple usage of numpy:
        # good for plotting, etc
        n_gin = n[n['abbrev']=='GIN']
        n_tea = n[n['abbrev']=='TEA']

        # Other usages:
        # q = n['quantity']
        # p = n['price']
        # bs = n['buysell']
        # com = n['abbrev']  #company
        # #q[com=='GIN']
        # #print q.shape

        # All prices are 1.0 for now.
        weighted_mean = NumpyTrades.calculate_volume_weighted_stock_price(n_gin)
        geometric_mean = NumpyTrades.calculate_geometric_mean(n)
        print {'weighted_mean': weighted_mean, 'geometric_mean':geometric_mean}
        TestUtils.assertFloatEqual(self, weighted_mean, 1.0)
        TestUtils.assertFloatEqual(self, geometric_mean, 1.0)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()
