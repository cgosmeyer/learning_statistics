""" Verification tests for the two-sample difference classes.

Author:
    
    C.M. Gosmeyer

Date:

    Mar 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe

"""

import pytest
from stats.inferential_stats.twosample import *

class TestZTest(object):
    """ Uses table 10.1.
    """
    def setup(self):
        n1 = 15
        n2 = 45
        mean1 = 52.6
        mean2 = 51.2
        s1 = 7.82
        s2 = 16.5
        return ZTest(n1, n2, mean1, mean2, s1, s2)
    def test_standard_error(self):
        ztest = self.setup()
        val = round(ztest.sigma_x1subx2, 2)
        assert val == 3.18
    def test_t(self):
        ztest = self.setup()
        val = round(ztest.test_stat, 2)
        assert val == 0.44

class TestWilcoxonRankSum(object):
    """ Uses table 10.2.
    """
    def setup(self):
        n1 = 15
        n2 = 45
        W1 = 473.5
        W2 = 1356.5
        return WilcoxonRankSum(n1, n2, W1, W2)
    def test_standard_error(self):
        wtest = self.setup()
        val = round(wtest.s_w, 2)
        assert val == 58.58
    def test_mean_rank1(self):
        wtest = self.setup()
        mean_rank1 = wtest.mean_rank_W(15)
        val = round(mean_rank1, 1)
        assert val == 457.5
    def test_Zw(self):
        wtest = self.setup()
        val = round(wtest.test_stat, 2)
        assert val == 0.27

class TestDiffOfProportions(object):
    """ Uses table 10.5.
    """
    def setup(self):
        n1 = 2156
        n2 = 7269
        p1 = 0.2393
        p2 = 0.3285
        return DiffOfProportions(n1, n2, p1, p2)
    def test_pooled_estimate(self):
        ptest = self.setup()
        val = round(ptest.pooled_estimate, 3)
        assert val == 0.308        
    def test_standard_error(self):
        ptest = self.setup()
        val = round(ptest.sigma_p1subp2, 3)
        assert val == .011
    def test_Zp(self):
        ptest = self.setup()
        val = round(ptest.test_stat, 2)
        assert val == 7.88     
