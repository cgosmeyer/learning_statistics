""" Functions for inferential classical hypothesis tests.

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


class ClassicalHypothesis(object):

    def __init__(self, hyp_val, val, n, stddev, alpha, rejection):
        """

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
        alpha : float
            Pre-determined significance level. 0.05 - 0.10 are most
            conventional.
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
        self.alpha = alpha
        self.rejection = rejection

        self.test_stat = self.test_statistic()
        self.decision = self.make_decision()

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

    def make_decision(self):
        """ Make decision regarding null and alternate hypothesis.

        Returns
        -------
        decision : {True, False}
            Rejection or acceptance of null hypothesis.
        """
        # Calculate rejection region
        rejection_region = self.alpha / float(self.rejection)

        # Calculate critical value.
        if self.n >= 30:
            # Should use rejection region to look up appropriate Z-value.
            # Let's say it is roughly
            critical_value = 1.65  # +/-
        elif self.n < 30:
            # Should use rejection region to look up appropriate t-value
            # for given n. Let's say it is roughly 
            critical_value = 2.06  # +/-
        
        # Make decision to accept (True) or reject (False).
        # Always assume null hypothesis is True.
        decision = True
        if abs(self.test_stat) >= critical_value:
            decision = False

        return decision

class OneSampleDifferenceMeans(ClassicalHypothesis):
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
    def __init__(self, hyp_mean, mean, n, stddev, alpha, rejection):
        ClassicalHypothesis.__init__(self, hyp_mean, mean, n, stddev, alpha, rejection)
        self.hyp_mean = hyp_mean
        self.mean = mean

