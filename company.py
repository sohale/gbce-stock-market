""" Company """

from gbce_utils import GBCEUtils

class CompanyEntry(object):

    class CT():
        """ Company types """
        COMMON = 2345
        PREFERRED = 6789

    def __init__(self, abbrev, company_type, last_dividend, fixed_dividend, par_value):
        self.ct = company_type
        if not self._type_preferred():
            assert fixed_dividend is None
            self.fixed_dividend = None
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

        if not GBCEUtils.type_is_int(self.par_value):
            raise Exception("Par Value has to be int. It is "+repr(self.par_value)+" of type " + str(type(self.par_value)))

        #todo: more

        return True  # enable `assert` usage

    def _type_preferred(self):
        if self.ct == CompanyEntry.CT.COMMON:
            return False
        elif self.ct == CompanyEntry.CT.PREFERRED:
            return True
        else:
           raise Exception("Unknown company type")
        
    def calculate_dividend_yield():
        """ calculate the Divident Yield based on the given market price.
        This is one of the endpoints."""
        if self.ct == CompanyEntry.CT.COMMON:
            pass
        elif self.ct == CompanyEntry.CT.PREFERRED:
            pass

