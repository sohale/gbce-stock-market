import numpy as np

class GBCEUtils(object):
    """ Utility functions, a static class that is simply a collection of static functions. """

    @staticmethod
    def type_is_int(value):
        return type(value) == int  or  type(value) == np.int32
