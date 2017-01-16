#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2 as unittest
import numpy as np

from trade import Trade

# assert np.version.full_version >= '1.11.2'

class TradeTest(unittest.TestCase):
    def test1(self):
        self.assertTrue(False)
        """ Contains multiple unit test."""
        # Todo: should be in Pence (hundredth of a Pound, or in Pounds (GBP) with wo decimals)
        t = Trade(timestamp=np.datetime64('2005-02-25', 'ms'), quantity=13, buysell_type=Trade.BUY, trade_price=1.00)
        t.check()
        print repr(t.numpy())
        print repr(t.numpy().shape)
        assert t.invar()
        #print np.datetime64('2005-02-25')
        assert t.timestamp - np.datetime64('2005-02-25','ms')  == np.timedelta64(0,'ms')
        assert t.quantity == 13
        assert type(t.quantity) == int
        print repr(Trade.numpy_2_trade(t.numpy()))
        recoded = Trade.numpy_2_trade(t.numpy())
        print str(recoded)
        print recoded, t, recoded == t

        assert t == Trade.numpy_2_trade(t.numpy())  # timestamp's units

def some_doctests():
    return "OK"

if __name__ == '__main__':
    import doctest
    doctest.testmod()

