""" Verification test for nearest neighbor analysis.

Author:
    
    C.M. Gosmeyer

Date:

    Mar 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe

"""

import pytest
from stats.inferential_spatial_stats.nearest_neighbor import *
from stats.inferential_stats.pvalue import PValue

class TestNearestNeighbor(object):
    """ Uses tables 14.1 and 14.2.
    """

    def setup_1(self):
        x_pos = [ 1.3,  3.2,  3.3,  5.6,  4.8,  8.1,  9.4]
        y_pos = [ 0.9,  4.4,  6.4,  3.8,  2.7,  7.4,  3.4]
        area = 1
        return NearestNeighbor(area=area, x_pos=x_pos, y_pos=y_pos)

    def test_NND(self):
        nn = self.setup_1()
        NND = round(nn.NND, 2)
        assert NND == 2.67

    def setup_2(self):
        NND = 3.63
        n = 20
        area = 641.45
        return NearestNeighbor(area=area, NND=NND, n=n)

    def test_NND_R(self):
        nn = self.setup_2()
        NND_R = round(nn.NND_R, 2)
        assert NND_R == 2.83

    def test_R(self):
        nn = self.setup_2()
        R = round(nn.R, 2)
        assert R == 1.28

    def test_standard_error(self):
        nn = self.setup_2()
        sigma_NND = round(nn.sigma_NND, 2)
        assert sigma_NND == 0.33

    def test_Z_n(self):
        nn = self.setup_2()
        Z_n = round(nn.Z_n, 2)
        assert Z_n == 2.41

    def test_pvalue(self):
        nn = self.setup_2()
        Z_n = round(nn.Z_n, 2)
        pvalue = round(PValue(Z_n, 20, rejection=1, min_n=20).pvalue, 3)
        assert pvalue == 0.008

