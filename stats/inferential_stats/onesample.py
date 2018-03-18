""" One-sample p-value tests.

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
from pvalue import PValue

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