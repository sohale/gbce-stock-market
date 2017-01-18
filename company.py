class CompanyEntry(object):

   class CT():
      """ Company types """
      COMMON = 2345
      PREFERRED = 6789

   def __init__(self, abbrev, company_type, last_dividend, fixed_dividend, par_value):
      self.ct = company_type
      assert self.check()

   def check(self):
      """ Class invariant. Asserts consistency of data in this object. """
      if self.ct == CompanyEntry.CT.COMMON:
          pass
      elif self.ct == CompanyEntry.CT.PREFERRED:
          pass
      else:
          raise Exception("Company type can only be either CT.COMMON or CTPREFERRED ")

      #todo: more

      return True  # enable `assert` usage

   def calculate_dividend_yield():
      if self.ct == CompanyEntry.CT.COMMON:
          pass
      elif self.ct == CompanyEntry.CT.PREFERRED:
          pass

