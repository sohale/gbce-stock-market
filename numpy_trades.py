
import numpy as np

class NumpyTrades(object):
    """
    NumpyTrades: a class for numpy format of storing in memoey. Efficient for fast (batch) calculations
    
    NumpyTrades is a static class with operations on numpy AoS; Array of Structure format. 
    Also see TradeSeries.calculate_* methods.


    
    The structure is according to Trade.numpy_dtype:    
        numpy_dtype = [('timestamp', 'datetime64[ms]'),('quantity', 'i4'), ('buysell', 'b1'), ('price', 'f4'), ('abbrev', 'S3')]
    """

    @staticmethod
    def calculate_volume_weighted_stock_price(numpy_aos):
        """ Weighted Mean """
        q = numpy_aos['quantity']
        p = numpy_aos['price']
        bs = numpy_aos['buysell']
        return sum(q[bs] * p[bs]) / sum(q[bs])

    @staticmethod
    def calculate_geometric_mean(numpy_aos):
        """ Geometric mean """
        q = numpy_aos['quantity']
        p = numpy_aos['price']
        bs = numpy_aos['buysell']

        assert sum(q[bs] <= 0) == 0  # All q are positive
        return np.exp(sum(q[bs] * np.log(p[bs])) / sum(q[bs]))
