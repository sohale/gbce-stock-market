
from trade import Trade
from trade_series import TradeSeries
# from company import CompanyEntry

class Market(object):
    """ List of companies. Also holds a TradeSeries for them."""
    def __init__(self):
        self.companies_dict = {}
        self.trade_sries = TradeSeries()

    # fixme: select those companies only based on their three-etter code
    @staticmethod
    def lookup_company1(company_abbr, companies_list):
        assert len(company_abbr) == 3
        assert type(companies_list) is dict
        for abbrev,c in companies_list.iteritems():
            assert abbrev == c.abbrev
            if c.abbrev == company_abbr:
                return c
        raise Exception("company not found from the name (abbreviation): "+repr(company_abbr))

    def lookup_company2(self, company_abbr):
        return Market.lookup_company1(company_abbr, self.companies_dict)

    @staticmethod
    def numpy_2_trade(numpy_arr, companies_dict):
        assert numpy_arr.shape == (1,)

        # fixme: select those companies only based on their three-etter code
        def one_trade_element(numpy_arr, i):
            abbrv = numpy_arr[i]['abbrev']
            company = Market.lookup_company1(abbrv, companies_dict)
            obj = Trade(company, numpy_arr[i]['timestamp'], numpy_arr[i]['quantity'], numpy_arr[i]['buysell'], numpy_arr[i]['price'])
            obj.check()
            return obj

        i = 0
        return one_trade_element(numpy_arr, i)
