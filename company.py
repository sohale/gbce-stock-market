#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Company """

from gbce_utils import TypeUtils
from gbce_utils import CurrencyUtils

class CompanyEntry(object):

    class CT(object):
        """ Company types """
        COMMON = 2345
        PREFERRED = 6789

    def __init__(self, abbrev, company_type, last_dividend, fixed_dividend, par_value):
        """
        @param par_value:  aka face value or nominal value of a bond/stock.
        Par value is a per share amount appearing on stock certificates as well as bond certificates.
        Units: Par value for a bond is typically $1,000 or $100 (in US).

        COMMON Stock:
        In the case of common stock the par value per share is usually a very small amount such as $0.10 or $0.01 or $0.001 and it has no connection to the market value of the share of stock
        It is not often mentioned for the `common stock` because it is arbitrary.
        The par Value is a static value, unlike `market value` which can fluctuate on a daily basis.
        ref: http://www.investopedia.com/terms/a/at-par.asp


        PREFERRED Stock:
        It (Par Value) determins a fixed-income (for coupons).
        The fixed annual payment := coupon rate * Par Value (both fixed).
        It determins the maturity value, that is(?); (coupon rate 100%) * Par Value.
        Is fixed_dividend = the coupon rate?

        @param company_type: Common Stock or PREFERRED Stock
        """
        self.ct = company_type
        if not self._type_preferred():
            assert fixed_dividend is None
            self.fixed_dividend = None
        else:
            self.fixed_dividend = fixed_dividend / 100.0
        self.abbrev = abbrev
        self.last_dividend = last_dividend
        self.par_value = par_value
        self.check()

    def __repr__(self):
        if self._type_preferred():
            # PREFERRED
            return self.abbrev + " (P: %" +str((self.fixed_dividend) * 100)+" x ParV:" + CurrencyUtils.GBP_symbol+ str(self.par_value) + ")"
        else:
            # COMMON
            #return "OK"
            return self.abbrev + " (C: " + CurrencyUtils.GBP_symbol + ('%.2f' %(self.last_dividend)) + ")"

    def check(self):
        """ Class invariant. Asserts consistency of data in this object. """
        if self.ct == CompanyEntry.CT.COMMON:
            pass
        elif self.ct == CompanyEntry.CT.PREFERRED:
            pass
        else:
            raise Exception("Company type can only be either CT.COMMON or CT.PREFERRED ")

        if not self._type_preferred():
            if self.fixed_dividend is not None:
                raise Exception("fixed_dividend has to be None for PREFERRED Sock company type.")
        else:
            if self.fixed_dividend is None:
                raise Exception("fixed_dividend cannot be None for COMMON Stock company type. "+repr(self.fixed_dividend))
            if not (self.fixed_dividend >= 0.0 and self.fixed_dividend <= 1.0):
                raise Exception("fixed_dividend has to be a real number between 0%, 100% (i.e. between 0.0 and 1.0). " + str(self.fixed_dividend*100.0)+" %")

        if not TypeUtils.type_is_int(self.par_value):
            raise Exception("Par Value has to be int. It is "+repr(self.par_value)+" of type " + str(type(self.par_value)))

        if not self.par_value > 0:
            raise Exception("Par Value has to be positive non zero. " + repr(self.par_value))

        if not len(self.abbrev) == 3:
            raise Exception("Company name has to be three letters. " + repr(self.abbrev))

        if not self.last_dividend >= 0:
            raise Exception("Company last_dividend has to be a non-negative real value. " + repr(self.last_dividend))

        #todo: more

        return True  # enable `assert` usage

    def _type_preferred(self):
        if self.ct == CompanyEntry.CT.COMMON:
            return False
        elif self.ct == CompanyEntry.CT.PREFERRED:
            return True
        else:
            raise Exception("Unknown company type")

    def calculate_dividend_yield(self, market_price):
        """ calculate the Divident Yield based on the given market price.
        This is one of the endpoints.
        @param market_price: Provided as an input becuase it is dynamic. Other object fields are static (no time-series for them). See documents for self.par_value
        """
        if self.ct == CompanyEntry.CT.COMMON:
            # The "Pal Value" is ignored. Also fixed_dividend is ignored?
            return self.last_dividend / market_price
        elif self.ct == CompanyEntry.CT.PREFERRED:
            # is 'last_dividend' ignored?
            return self.fixed_dividend * self.par_value / market_price

    def PE_ratio(self, market_share_price):
        """ I am very unsure about this. Domain knowledge is required. I write it based on my best judgement.
        Problem: Division by zero.

        Market Value per Share / Earnings per Share.
        EPS is most often derived from the last four quarters.
        The price-earnings ratio (P/E Ratio) is the ratio for valuing a company that measures its current share price relative to its per-share earnings.
        The price-earnings ratio   :=   Market Value per Share / Earnings per Share
        Ref: http://www.investopedia.com/terms/p/price-earningsratio.asp

        Specified in the assignment: PE = market_price / dividend

        Question: What is dividend is zero; e.g. a Common Stock where Last Dividened is zero (see example 'TEA').

        @param market_share_price: aka market_price, Market Value per Share.
        """
        dividend = self.calculate_dividend_yield(market_share_price)
        earnings_per_share = dividend
        #assert dividend > 0, "dividend cannot be zero for P/E ratio " + repr(dividend)
        if not dividend > 0:
            print "Warning: ", "Dividend cannot be zero for P/E ratio " + repr(dividend)
            return -1.0
        return market_share_price / earnings_per_share

    def report_company_info(self, market_share_price):
        return repr(self) + "  ......  P/E=" + str(self.PE_ratio(market_share_price)) + " ...... DivYield=" + CurrencyUtils.GBP_symbol + str(self.calculate_dividend_yield(market_share_price))
