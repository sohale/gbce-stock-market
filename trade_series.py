#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" TradeSeries, a sorted set of trades in a GBCE Stock Exchange. """

import math

from trade import Trade
from gbce_utils import TimeUtils

class TradeSeries(object):
    """ An array of Trades, uses 'list' containting instances of a Trade class. 
    Ther are alternative representations possible. See the get_numpy() method."""

    def __init__(self):
        """ Initialises an empty series """
        self.all_trades = []


    def get_numpy(self):
        """ AoS: Array-of-Structure version for/in numpy."""
        return Trade.numpy_array(self.all_trades, use_rec=False)

    def get_numpy_rec(self):
        """ SoA: Structure-of-Array version for/in numpy. It is also known as `record` or `numpy.rec.array` in numpy."""
        return Trade.numpy_array(self.all_trades, use_rec=True)

    def _select_recent_trades(self, from_ms, to_ms, company_code):
        """ Selected a set of Trades in the given interval. Generator version. Thre usages:
        
        ts._select_recent_trades(from_ms, to_ms, company_code) # selects trades of a company that are within an interval 
        ts._select_recent_trades(from_ms, to_ms, None)  # selects the trades in a given interval regardless of the company. For a specifi history length, use select_recent_trades() instead.
        ts._select_recent_trades(None, None, company_code)  # selects trades of the given company
        """
        if from_ms == None and to_ms == None:
            skip_time_interval = True
        else:
            skip_time_interval = False

        if company_code is None:
            skip_company = True
        else:
            skip_company = False

        if not skip_time_interval:
            if from_ms > to_ms:
                raise Exception("Usage error: Incorrect range.start is after end end of the time interval's range.")
            if from_ms == to_ms:
                raise Exception("Usage error: Empty range. The end of the range is not inclusive.")

        for t in self.all_trades:
            if skip_time_interval or (t.timestamp >= from_ms and t.timestamp < to_ms):
                if skip_company or (t.company_obj is not None and t.company_obj.abbrev == company_code):
                    yield t

    def select_recent_trades(self, time_diff_ms, company_code): #(from_ms, to_ms=0):
        """ Makes a collection of Trades in the given length of history. Generator version.
        Warning: the end of the range is not inclusive. """

        numpy_time_now_ms = TimeUtils.numpy_time_now() #np.datetime64(datetime.datetime.now(), 'ms')
        from_ms = numpy_time_now_ms - TimeUtils.numpy_time_delta_msec(time_diff_ms)
        #raise Exception("Not implemented "+str(from_ms)+" "+str(now_ms))
        return self._select_recent_trades(from_ms, numpy_time_now_ms, company_code)

    def select_company_trades(self, company_code):
        """ Makes a collection of Trades for a specific company.
        If you need a pecifict company and a specific time range, used _select_recent_trades() instead.
        """
        return self._select_recent_trades(None, None, company_code)

    def select_all_trades(self):
        """ Selects all trades, all companies. For All-Index, etc. Equivalent to returning self.all_trades 
        """
        return self._select_recent_trades(None, None, None)

    VERBOSE = True

    @staticmethod
    def calculate_volume_weighted_stock_price(trades_iterable):
        """
        Volume Weighted Stock Price
        """
        if TradeSeries.VERBOSE:
            weighted_price_str = []
            sum_weights_str = []
            print

        weighted_price = 0.0
        sum_weights = 0.0
        for trade in trades_iterable:
            weighted_price += trade.quantity * trade.price
            sum_weights += trade.quantity

            if TradeSeries.VERBOSE:
                weighted_price_str.append(str(trade.quantity)+ "x" + str(trade.price))
                sum_weights_str.append(str(trade.quantity))

        if TradeSeries.VERBOSE:
            print ":", " + ".join(weighted_price_str)
            cnt = len(weighted_price_str) + 5
            print "-" * (2*cnt), " div ", "-"*(2*cnt) 
            print ":", " + ".join(sum_weights_str)

        if sum_weights == 0.0:
            raise Exception("No trade, sum(quantity) is zero.")
        return weighted_price / sum_weights

    @staticmethod
    def calculate_geometric_mean(trades_iterable):
        """
        Calculate the GBCE All-Share Index using the geometric mean of prices for all stocks
        """
        if TradeSeries.VERBOSE:
            weighted_price_str = []
            sum_weights_str = []
            print

        weighted_logprice = 0.0
        sum_weights = 0.0
        for trade in trades_iterable:
            # log(trade.price) is always defined because the Trade.check() guarantees it.
            weighted_logprice += trade.quantity * math.log(trade.price)
            sum_weights += trade.quantity

            if TradeSeries.VERBOSE:
                weighted_price_str.append(str(trade.price) + "^" + str(trade.quantity) )
                sum_weights_str.append(str(trade.quantity))

        if TradeSeries.VERBOSE:
            print "[", " * ".join(weighted_price_str) + "] ",
            cnt = len(weighted_price_str) + 5
            print " ^ 1  /  (",
            print " * ".join(sum_weights_str), "=", sum_weights,
            print ")"

        if sum_weights == 0.0:
            raise Exception("No trade, sum(quantity) is zero.")
        return math.exp(weighted_logprice / sum_weights)
