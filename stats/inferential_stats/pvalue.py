""" Base class for p-value test.

Author:
    
    C.M. Gosmeyer

Date:

    Mar 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe

"""

from __future__ import print_function

import numpy as np
import pandas as pd
from stats.tables.load_table import LoadNormalTable, LoadStudentsTTable


class PValue(object):

    def __init__(self, test_stat, n, rejection): #hyp_val, val, n, stddev, rejection):
        """ 
        If p-value near 1: Trust null hypothesis. ("our data is highly
           consistant with our hypothesis")
        If p-value near 0: Reject null hypothesis.

        Parameters
        ----------
        hyp_val : float
            Hypothesized value.
        val : float
            Population, or if unknown, sample value.
        n : int
            Sample size.
        stddev : float
            Population, or if unknown, sample standard deviation.
        rejection : int
            The rejection region of null-hypothesis.
            If 2, two-tailed, equals alpha/2 on each side.
            If 1, one-tailed, equals alpha on positive side.
            If -1, one-tailed, equals alpha on negative side.
        """

        #  null hypthesis : val - hyp_val = 0
        #self.hyp_val = hyp_val
        #self.val = val
        self.n = n
        #self.stddev = stddev
        self.rejection = rejection

        self.test_stat = test_stat #self.test_statistic()
        self.area = self.determine_probability_tail()
        self.pvalue = self.determine_rejection_area()

    #def test_statistic(self):
    #    """ Generalized test statistic.
    #
    #    Returns
    #    -------
    #    test_stat : float
    #        Test statistic.
    #    """
    #    if self.n >= 30:
    #        # Z
    #        test_stat = (self.val - self.hyp_val) / (self.stddev / np.sqrt(self.n))
    #    elif self.n < 30:
    #        # t
    #        test_stat = (self.val - self.hyp_val) / (self.stddev / np.sqrt(self.n - 1))
    #
    #    return test_stat

    def determine_probability_tail(self):
        """ Calculates probability (relative area) under one section of 
        normal curve for given test statistic.

        Returns
        -------
        area : float
            The area under one section of probability distribution curve.
        """
        # Need look up on Z or t table what the area should be. 
        if self.n >= 30:
            z_table = LoadNormalTable()
            area = z_table.find_prob(self.test_stat)
        elif self.n < 30:
            t_table = LoadStudentsTTable(tails=1)
            area = t_table.find_confidence(self.test_stat, df=self.n)
        #area = 0.5 - area
        return area

    def determine_rejection_area(self):
        """ Determine rejection area by subtracting probability from 0.5.
        This value is the p-value (area of tail).

        Returns
        -------
        pvalue : float
        """
        pvalue = 0.5 - self.area

        # Double area if two-tailed.
        pvalue *= self.rejection

        return pvalue

    def get_pvalue(self):
        print(self.pvalue)
    
