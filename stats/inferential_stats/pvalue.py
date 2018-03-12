""" Functions for inferential p-value tests.

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


class PValue(object):

    def __init__(self, hyp_val, val, n, stddev, rejection):
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
        self.hyp_val = hyp_val
        self.val = val
        self.n = n
        self.stddev = stddev
        self.rejection = rejection

        self.test_stat = self.test_statistic()
        self.area = self.determine_probability_tail()
        self.pvalue = self.determine_rejection_area()

    def test_statistic(self):
        """ Generalized test statistic.

        Returns
        -------
        test_stat : float
            Test statistic.
        """
        if self.n >= 30:
            # Z
            test_stat = (self.val - self.hyp_val) / (self.stddev / np.sqrt(self.n))
        elif self.n < 30:
            # t
            test_stat = (self.val - self.hyp_val) / (self.stddev / np.sqrt(self.n - 1))

        return test_stat

    def determine_probability_tail(self):
        """ Calculates probability (relative area) under each tail of 
        normal curve for given test statistic.

        Returns
        -------
        area : float
        """
        # Need look up on Z or t table what the area should be. 
        # for now, assume
        if self.n >= 30:
            area = 0.4495
        elif self.n < 30:
            area = 0.4715

        return area

    def determine_rejection_area(self):
        """ Determine rejection area by subtracting probability from 0.5.
        This value is the p-value.

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


class OneSampleDifferenceMeans(PValue):
    """ Compares a random sample mean to a popsulation mean for 
    difference.

    Requirements
    ------------
    1. Random sample
    2. Population from which sample is drawn is normally distributed.
    3. Variable is measured at interval or ratio scale.

    Null Hypthothesis
    -----------------
    sample mean = hythothesized mean

    Test Statistic
    --------------

        Z or t = SampleMean - PopulationMean / StandardErrorMean

        where

        StandardErrorMean = PopulationStandardDev / sqrt(SampleSize)

        and 

        if SampleSize < 30, use t
        if SampleSize >= 30, use Z
    """
    def __init__(self, hyp_mean, mean, n, stddev, rejection):
        PValue.__init__(self, hyp_mean, mean, n, stddev, rejection)
        self.hyp_mean = hyp_mean
        self.mean = mean

class OneSampleDifferenceProportions(PValue):
    """ Compares a random sample proportion to a population proportion 
    for difference.

    Requirements
    ------------
    1. Random sample
    2. Variable is organized by dichotomous (binary) categories.

    Null Hypthothesis
    -----------------
    sample proportion = hythothesized proportion

    Test Statistic
    --------------

        Z or t = SampleProportion - PopulationProportion / StandardErrorProportion

        where

        StandardErrorProportion = sqrt(SampleProportion * (1 - SampleProportion) / SampleSize)

        and 

        if SampleSize < 30, use t
        if SampleSize >= 30, use Z
    """
    def __init__(self, hyp_prop, prop, n, stddev, rejection):
        PValue.__init__(self, hyp_prop, prop, n, stddev, rejection)
        self.hyp_prop = hyp_prop
        self.prop = prop

    def test_statistic(self):
        if self.n >= 30:
            # Z
            test_stat = (self.hyp_val - self.val) / np.sqrt(self.hyp_val*(1-self.hyp_val)/self.n)
        elif self.n < 30:
            # t
            test_stat = (self.hyp_val - self.val) / np.sqrt(self.hyp_val*(1-self.hyp_val)/(self.n-1))

        return test_stat        
