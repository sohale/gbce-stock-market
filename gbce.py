#!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" GBCS Stock Demo """
import sys
from company import CompanyEntry
from market import Market

def demo_get15min():
    print 'Please run "python tests.py" instead'

class commandline(object):
    """ A static class for offline operations. """

    @staticmethod
    def init():
        market = Market()
        market.store_on_disk()

    @staticmethod
    def show():
        market = Market.load_from_disk()
        print repr(market)

    @staticmethod
    def company(*args):
        print args
        market = Market.load_from_disk()
        abbrev = args[0]
        if not abbrev.upper() == abbrev:
            raise Exception("Company abbreviation has to be uppercase")
        if not len(abbrev) == 3:
            raise Exception("Company abbreviation has to be three letters")
        company_type = CompanyEntry.CT.COMMON
        fixed_dividend = None
        last_dividend = float(args[1])
        par_value = int(args[2])
        assert len(args) == 3
        c = CompanyEntry(abbrev, company_type, last_dividend, fixed_dividend, par_value)
        c.check()  # crucial
        if c.abbrev in market.companies_dict:
            raise Exception("Company exists with same abbreviations: "+repr(args)+"   Company:"+repr(c))
        print "Adding company: ", repr(c)
        market.companies_dict[c.abbrev] = c
        print "Market Summary:"
        #print "---------------"
        print "        ", repr(market)
        market.store_on_disk()
        print "Stored on disk successfully."

functions_lookup = {
        'init': commandline.init,
        'company': commandline.company,
        'show': commandline.show,
    }

if __name__ == "__main__":
    # demo_get15min()
    #print repr(sys.argv)  # ['p1.py', 'company', 'ABC', '12', '50']
    commandname = sys.argv[1]
    xargs = sys.argv[2:]
    # commandline.init()
    #commandline.show()
    #commandline.company(*(sys.argv[1:]))
    if not commandname in functions_lookup:
        raise Exception("unknown command. available commands: "+(", ".join(functions_lookup.keys())))
    func = functions_lookup[commandname]
    print "COMMAND: ", commandname
    func(*xargs)

