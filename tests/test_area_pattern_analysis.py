""" Verification tests for area pattern analysis tests Joint Count 
(binary) and Moran's Index.

Author:
    
    C.M. Gosmeyer

Date:

    Apr 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe

"""

import pytest
from stats.inferential_spatial_stats.area_pattern_analysis import *
from stats.inferential_stats.pvalue import PValue

class TestJointCountBinary(object):
    """ Uses tables 15.3 and 15.4.
    """
    def setup(self):
        B = 26
        W = 22
        J = 106
        link_list = [4,5,6,3,7,3,3,2,5,6,5,4,6,4,7,3,1,4,5,2,4,4,8,4,6,5,3,3,5,5,4,3,5,6,4,6,2,2,6,8,4,6,3,5,2,5,4,6]
        observed_joins = 21
        return JointCountBinary(B, W, J, link_list, observed_joins)

    def test_Ebw(self):
        jcb = self.setup()
        Ebw = round(jcb.expected_joins, 2)
        assert Ebw == 53.75

    def test_sigma(self):
        jcb = self.setup()
        sigma = round(jcb.sigma_expected_joins, 2)
        assert sigma == 4.92

    def test_Zb(self):
        jcb = self.setup()
        test_stat = round(jcb.test_stat, 2)
        assert test_stat == -6.66    

