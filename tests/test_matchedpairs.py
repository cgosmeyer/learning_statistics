""" Verification tests for the matched-pairs classes.

Author:
    
    C.M. Gosmeyer

Date:

    Mar 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe

"""

import pytest
from stats.inferential_stats.matchedpairs import *

class TestTTest(object):
    """ Uses table 10.6.
    """
    def setup(self):
        n = 10
        x = [5.2, 5.3, 5.8, 4.1, 4.8, 5.2, 4.7, 4.9, 4.9, 4.5]
        y = [5.8, 5.8, 7.3, 6.7, 6.7, 7, 7, 5.8, 7.4, 5.1]
        return TTest(n, x, y)

    def test_mean_differences(self):
        ttest = self.setup()
        val = round(ttest.d, 2)
        assert val == 1.52

    def test_standard_error(self):
        ttest = self.setup()
        val = round(ttest.sigma, 2)
        assert val == 0.27  # 0.82 / sqrt(10-1)

    def test_T_mp(self):
        ttest = self.setup()
        val = round(ttest.test_stat, 2)
        assert val == 5.55  # book said 2.96, but math doesn't work

class TestWilcoxonSignedRanks(object):
   def setup(self):
       Tp = 19
       Tn = 47
       n = 11
       return WilcoxonSignedRanks(n, Tp, Tn)

   def test_T(self):
       Zwtest = self.setup()
       assert Zwtest.T == 19  # should be minimum

   def test_Zw(self):
       Zwtest = self.setup()
       val = round(Zwtest.test_stat, 2)
       assert val == -1.24
