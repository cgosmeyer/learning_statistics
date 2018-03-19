""" Dependent-sample (matched pair) tests.

Author:
    
    C.M. Gosmeyer

Date:

    Mar 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe

"""

import numpy as np


class MatchedPairs(object):
    """ Base class for matched-pairs tests.
    """
    def __init__(self, n):

        """
        Parameters
        ----------
        n : int
            Size of matched-pairs sample.
        """

        self.n = float(n)

class TTest(MatchedPairs):
    """ Compares matched pairs from a random sample for difference.

    Requirements
    ------------
    1. Random sample.
    2. Data are collected for two different samples or at two different
       time periods.
    3. Population is normally distributed.
    4. Variable(s) is (are) measured at interval or ratio scale.

    Null Hypthothesis
    -----------------
    PopulationMatched-PairMeanDifference = 0

    Test Statistic
    --------------
    
        t_mp = MeanOfMatched-PairDifferences / StandErrorOfMeanDifference

        where

        MeanOfMatched-PairDifferences = sum(DifferencesForMatchedPair_i) /
                                         NumberOfMatchedPairs

        and

        StandErrorOfMeanDifference = VarianceOfMatchedPair / sqrt(NumberSamples)

        where

        VarianceOfMatchedPair = sqrt( sum(DifferencesForMatchedPair_i - MeanOfMatched-PairDifferences)^2 /
                                       (NumberSamples - 1))


    """
    def __init__(self, n, x, y):
        MatchedPairs.__init__(self, n)
        """
        Parameters
        ----------
        x : array
            First variable in matched-pairs.
        y : array
            Second variable in matched-pairs.
        """
        self.x = np.asarray(x)
        self.y = np.asarray(y)
        self.d = self.mean_differences()
        self.sigma = self.standard_error()
        self.t_mp = None
        self.test_statistic()
        self.test_stat = self.t_mp

    def mean_differences(self):
        """
        """
        d = abs(np.mean(self.x) - np.mean(self.y))
        return d

    def standard_error(self):
        """
        """
        d_i_2 = np.array([(self.x[i] - self.y[i])**2 for i in range(len(self.x))])
        d_i = np.array([abs(self.x[i] - self.y[i]) for i in range(len(self.x))])
        s = np.sqrt( (sum(d_i_2) - ((sum(d_i))**2 / self.n )) / (self.n - 1) )
        if self.n <= 10:
            sigma = s / np.sqrt(self.n - 1)
        else:
            sigma = s / np.sqrt(self.n)
        return sigma

    def test_statistic(self):
        """
        """
        self.t_mp = self.d / self.sigma

    def get_t_mp(self):
        print(self.t_mp)


class WilcoxonSignedRanks(MatchedPairs):
    """ Compares matched pairs from a random sample for difference.

    Requirements
    ------------
    1. Random sample.
    2. Data are collected for two different samples or at two different
       time periods.
    3. Population not necessarily normal or sample size not large.
    4. Variable(s) is (are) measured at ordinal scale or downgraded
       from interval/ratio scale to ordinal.

    Null Hypthothesis
    -----------------
    Ranked matched-pair differences of the population are normal.

    Test Statistic
    --------------
    
        Z_w = [RankSum - SampleSize * (SampleSize + 1) / 4] /
              sqrt( SampleSize * (SampleSize + 1) * (2*SampleSize + 1) / 24)

        where 

        RankSum = min(PostiveRankeSum, NegativeRankSum)


    """
    def __init__(self, n, Tp, Tn):
        MatchedPairs.__init__(self, n)
        """
        Parameters
        ----------
        Tn : int
            Ranked sum of negative differences.
        Tp : int
            Ranked sum of positive differences.
        """
        self.Tn = Tn
        self.Tp = Tp
        self.T = np.min([Tn, Tp])
        self.Zw = None

        if self.n > 10:
            self.test_statistic()

        self.test_stat = self.Zw

    def test_statistic(self):
        """
        """
        T = self.T
        n = self.n
        self.Zw = (T - n*(n + 1) / 4.0)/ \
            np.sqrt( n*(n + 1)*(2*n + 1)/24.0 )

    def get_Zw(self):
        print(self.Zw)
