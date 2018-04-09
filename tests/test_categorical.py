""" Verification tests for the categorical difference tests.

Author:
    
    C.M. Gosmeyer

Date:

    Mar 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe

"""

import numpy as np
import pytest
from stats.inferential_stats.categorical import *
from stats.inferential_stats.pvalue import PValue

class TestChiSquare(object):
    """ Uses table 12.1
    """
    def setup(self):
        FC_o = [42, 45, 51, 47, 60]
        FC_e = [49, 49, 49, 49, 49]
        return ChiSquare(FC_o, FC_e)
    
    def test_chi_square(self):
        ChiSqaretest = self.setup()
        val = round(ChiSqaretest.test_stat, 2)
        assert val == 3.96

    def test_pvalue(self):
        ChiSqaretest = self.setup()
        chi_square = round(ChiSqaretest.test_stat, 2)
        p = PValue(test_stat=chi_square, n=5, chi_square=True)
        pvalue = round(p.pvalue, 2)
        assert pvalue == 0.41       


class TestKolmogorovSmirnov(object):
    NotImplemented

class TestContingency(object):
    """ Uses table 12.6
    """
    def setup(self):
        FC_o = [[60, 70], [36, 33]]
        return Contingency(FC_o)
    
    def test_FC_e(self):
        Contingencytest = self.setup()
        val = round(Contingencytest.FC_e[0][0], 1)
        assert val == 62.7

    def test_chi_square(self):
        Contingencytest = self.setup()
        val = round(Contingencytest.test_stat, 2)
        assert val == 0.65


