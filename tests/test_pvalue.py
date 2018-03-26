""" Validation tests for the p-value test.

Author:
    
    C.M. Gosmeyer

Date:

    Mar 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe

"""

import pytest
from stats.inferential_stats.pvalue import *


class TestPValueNormalTable(object):
    """ Uses example 9.2.
    """
    def setup(self):
        test_stat = 1.45
        n = 85
        rejection = 1

        return PValue(test_stat, n, rejection)

    def test_normal_table_pvalue(self):
        test = self.setup()
        pvalue = test.pvalue
        assert pvalue == .0735


t = TestPValueNormalTable()
t.setup()