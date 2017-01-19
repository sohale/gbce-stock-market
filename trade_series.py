""" TradeSeries, a sorted set of trades in a GBCE Stock Exchange. """

from trade import Trade
from gbce_utils import TimeUtils

class TradeSeries(object):
    """ An array of Trades, uses 'list' containting instances of a Trade class. """

    def __init__(self):
        """ Initialises an empty series """
        self.all_trades = []


    def get_numpy(self):
        return Trade.numpy_array(self.all_trades, use_rec=False)

    def get_numpy_rec(self):
        return Trade.numpy_array(self.all_trades, use_rec=True)

    def _select_recent_trades(self, from_ms, to_ms):
        """ Selected a set of Trades in the given interval. Generator version. """
        if from_ms > to_ms:
            raise Exception("Usage error: Incorrect range.start is after end end of the time interval's range.")
        if from_ms == to_ms:
            raise Exception("Usage error: Empty range. The end of the range is not inclusive.")
        for t in self.all_trades:
            if t.timestamp >= from_ms and t.timestamp < to_ms:
                yield t

    def select_recent_trades(self, time_diff_ms): #(from_ms, to_ms=0):
        """ Makes a collection of Trades in the given length of history. Generator version.
        Warning: the end of the range is not inclusive. """

        numpy_time_now_ms = TimeUtils.numpy_time_now() #np.datetime64(datetime.datetime.now(), 'ms')
        from_ms = numpy_time_now_ms - TimeUtils.numpy_time_delta_msec(time_diff_ms)
        #raise Exception("Not implemented "+str(from_ms)+" "+str(now_ms))
        return self._select_recent_trades(from_ms, numpy_time_now_ms)

