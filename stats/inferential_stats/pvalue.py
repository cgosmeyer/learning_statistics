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

    def __init__(self, test_stat, n, rejection, min_n=30):
        """ 
        If p-value near 1: Trust null hypothesis. ("our data is highly
           consistant with our hypothesis")
        If p-value near 0: Reject null hypothesis.

        Parameters
        ----------
        test_stat : float
            The t or Z value from statistics test.
        n : int
            Sample size.
        rejection : int
            The rejection region of null-hypothesis.
            If 2, two-tailed, equals alpha/2 on each side.
            If 1, one-tailed, equals alpha on positive side.
            If -1, one-tailed, equals alpha on negative side.
        min_n : int
            The minimum n to use normal table. Nominally 30 for most 
            statistics test.
            Wilcoxon Matched-Pairs requires min_n=10.
        """
        self.test_stat = abs(test_stat)
        self.n = n
        self.rejection = rejection
        self.min_n = min_n

        self.area = self.determine_probability_tail()
        self.pvalue = self.determine_rejection_area()

    def determine_probability_tail(self):
        """ Calculates probability (relative area) under one section of 
        normal curve for given test statistic.

        Returns
        -------
        area : float
            The area under one section of probability distribution curve.
        """
        # Need look up on Z or t table what the area should be. 
        if self.n >= self.min_n:
            z_table = LoadNormalTable()
            area = z_table.find_prob(self.test_stat)
        elif self.n < self.min_n:
            t_table = LoadStudentsTTable(tails=1)
            area = t_table.find_confidence(self.test_stat, df=self.n)
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
    
