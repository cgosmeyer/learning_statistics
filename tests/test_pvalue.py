""" Verification tests for the p-value test.

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
    """ Uses example 9.2 and table 10.8.
    """
    def setup1(self):
        test_stat = 1.45
        n = 85
        rejection = 1
        return PValue(test_stat, n, rejection)

    def test_normal_table_pvalue(self):
        test = self.setup1()
        pvalue = round(test.pvalue, 4)
        assert pvalue == 0.0735

    def setup2(self):
        test_stat = -1.245
        n = 11
        rejection = 1
        min_n = 10
        return PValue(test_stat, n, rejection, min_n)

    def test_normal_table_area(self):
        test = self.setup2()
        area = test.area 
        assert area == 0.39435

    def test_normal_table_pvalue(self):
        test = self.setup2()
        pvalue = round(test.pvalue, 5)
        assert pvalue == 0.10565


class TestPValueStudentsTTable(object):
    """ Uses table 10.7.
    """
    def setup(self):
        test_stat = 2.96
        n = 10
        rejection = 1
        return PValue(test_stat, n, rejection)

    def test_students_t_table_pvalue(self):
        test = self.setup()
        pvalue = round(test.pvalue, 2)
        assert pvalue == 0.01


