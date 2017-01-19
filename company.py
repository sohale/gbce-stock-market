""" Company """

from gbce_utils import GBCEUtils

class CompanyEntry(object):

    class CT(object):
        """ Company types """
        COMMON = 2345
        PREFERRED = 6789

    def __init__(self, abbrev, company_type, last_dividend, fixed_dividend, par_value):
        self.ct = company_type
        if not self._type_preferred():
            assert fixed_dividend is None
            self.fixed_dividend = None
        else:
            self.fixed_dividend = fixed_dividend
        self.abbrev = abbrev
        self.last_dividend = last_dividend
        self.par_value = par_value
        self.check()

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
                raise Exception("fixed_dividend has to be None for PREFERRED company type.")
        else:
            if not (self.fixed_dividend >= 0 and self.fixed_dividend <= 100):
                raise Exception("fixed_dividend has to be a real number between 0, 100. " + repr(self.fixed_dividend))

        if not GBCEUtils.type_is_int(self.par_value):
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
        This is one of the endpoints."""
        if self.ct == CompanyEntry.CT.COMMON:
            return self.last_dividend / market_price
        elif self.ct == CompanyEntry.CT.PREFERRED:
            return self.last_dividend / market_price

