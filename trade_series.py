#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" TradeSeries, a sorted set of trades in a GBCE Stock Exchange. """

import math

from trade import Trade
from gbce_utils import TimeUtils

class TradeSeries(object):
    """ An array of Trades, uses 'list' containting instances of a Trade class. """

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
        """ Selected a set of Trades in the given interval. Generator version. """
        if from_ms > to_ms:
            raise Exception("Usage error: Incorrect range.start is after end end of the time interval's range.")
        if from_ms == to_ms:
            raise Exception("Usage error: Empty range. The end of the range is not inclusive.")
        for t in self.all_trades:
            if t.timestamp >= from_ms and t.timestamp < to_ms:
                if company_code is None or (t.company_obj is not None and t.company_obj.abbrev == company_code):
                    yield t

    def select_recent_trades(self, time_diff_ms, company_code): #(from_ms, to_ms=0):
        """ Makes a collection of Trades in the given length of history. Generator version.
        Warning: the end of the range is not inclusive. """

        numpy_time_now_ms = TimeUtils.numpy_time_now() #np.datetime64(datetime.datetime.now(), 'ms')
        from_ms = numpy_time_now_ms - TimeUtils.numpy_time_delta_msec(time_diff_ms)
        #raise Exception("Not implemented "+str(from_ms)+" "+str(now_ms))
        return self._select_recent_trades(from_ms, numpy_time_now_ms, company_code)

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
