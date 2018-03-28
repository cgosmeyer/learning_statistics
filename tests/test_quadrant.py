""" Verification test for quadrant analysis.

Author:
    
    C.M. Gosmeyer

Date:

    Mar 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe

"""

import pytest
from stats.inferential_spatial_stats.quadrant import *
from stats.inferential_stats.pvalue import PValue

class TestNearestNeighbor(object):
    """ Uses tables 14.4.
    """
    def setup(self):
        x = [11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,32,33]
        f = [1, 2, 2, 4, 3, 4, 9, 8, 15,10,10,11,9, 13,3, 2, 3, 8, 1, 2]
        return Quadrant(x, f)

    def test_variance(self):
        q = self.setup()
        var = round(q.var, 1)
        assert var == 18.9

    def test_chi_square(self):
        q = self.setup()
        chi_square = round(q.test_stat, 0)
        assert chi_square == 108

    def test_pvalue(self):
        q = self.setup()
        chi_square = round(q.test_stat, 2)
        p = PValue(test_stat=chi_square, n=120, chi_square=True)
        pvalue = p.pvalue 
        # This will only work if can interpolate table 
        # (but need a finer table for chi-square)
        assert pvalue == 0.77   
