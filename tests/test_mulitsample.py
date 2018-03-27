""" Verification tests for the multi-sample classes.

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
from stats.inferential_stats.multisample import *

class TestANOVA(object):
    """ Uses table 11.1.
    """
    def setup(self):
        means = np.array([28.780, 25.914, 30.609, 25.819])
        ns = np.array([65, 14, 90, 31])
        variances = np.array([1.544, 4.295, 3.006, 5.104])
        return ANOVA(means, ns, variances)
    
    def test_between_group_sum_of_squares(self):
        Ftest = self.setup()
        val = round(Ftest.SS_B, 1)
        assert val == 682.5

    def test_between_group_mean_squares(self):
        Ftest = self.setup()
        val = round(Ftest.MS_B, 1)
        assert val == 227.5

    def test_within_group_sum_of_squares(self):
        Ftest = self.setup()
        val = round(Ftest.SS_W, 0)
        assert val == 1978.0

    def test_within_group_mean_squares(self):
        Ftest = self.setup()
        val = round(Ftest.MS_W, 1)
        assert val == 10.1

    def test_F(self):
        Ftest = self.setup()
        val = round(Ftest.MS_W, 1)
        assert val == 10.1

class TestKruskalWallis(object):
    """ Uses tables 11.3 - 11.4.
    """
    def setup(self):
        rs = np.array([
            [17, 23, 5, 6, 22, 3, 12, 15, 10],
            [13.5, 19, 25.5, 33, 29, 21, 25.5, 27, 8, 30],
            [11, 2, 1, 9, 4, 18, 7, 16],
            [13.5, 24, 28, 31, 34, 32, 20]])
        return KruskalWallis(rs)

    def test_N(self):
        Htest = self.setup()
        val = Htest.N
        assert val == 34       

    def test_T(self):
        Htest = self.setup()
        val = Htest.T 
        assert val == 0

    def test_mean_rs1(self):
        Htest = self.setup()
        val = round(Htest.mean_rs[0], 1)
        assert val == 12.6   

    def test_sum_n_r(self):
        Htest = self.setup()
        val = round(Htest.sum_n_r, 1)
        assert val == 12114.0        

    def test_H(self):
        Htest = self.setup()
        val = round(Htest.H, 2)
        assert val == 17.16

