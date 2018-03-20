""" Multi-sample tests.

Author:
    
    C.M. Gosmeyer

Date:

    Mar 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe
"""

import numpy as np

class ANOVA(object):
    """ Compares three or more independent random sample means for
    difference.

    Requirements
    ------------
    1. Three or more (k) random samples.
    2. Each population *normally* distributed.
    3. Each population has *equal* variance.
    4. Variable is measured at interval or ratio scale.

    Null Hypthothesis
    -----------------
    mean1 = mean2 = ... = meank

    Test Statistic
    --------------

        F = BetweenGroupMeanSquares / WithinGroupMeanSquares

        where

        BetweenGroupMeanSquares = BetweenGroupSumOfSquares / (NumberSamples - 1)

        where 

        BetweenGroupSumOfSquares = sum( NumberObservationsInSample_i * 
                                       (MeanOfSample_i - OverallMean)^2 )

        where
        
        OverallMean = sum( NumberObservationsInSample_i * MeanOfSample_i /
                           TotalNumberObservationsInAllSamples)

        and 

        WithinGroupMeanSquares = WithinGroupSumOfSquares / 
                                 (TotalNumberObservationsInAllSamples - NumberSamples)

        where

        WithinGroupSumOfSquares = sum( (NumberObservationsInSample_i - 1) *
                                      VarianceSample_i^2 )      
    """                         
    def __init__(self, means, ns, variances):
        """
        Parameters
        ----------
        means : array
            Mean of each sample.
        ns : array
            Number of observations in each sample.
        variances : array
            Variance of each sample.
        """
        self.means = np.asarray(means)
        self.ns = np.asarray(ns)
        self.variances = np.asarray(variances)
        self.k = len(means)
        self.N = sum(ns)
        self.F = None
        self.SS_B = self.between_group_sum_of_squares()
        self.SS_W = self.within_group_sum_of_squares()
        self.MS_B = self.between_group_mean_squares()
        self.MS_W = self.within_group_mean_squares()

        self.test_statistic()
        self.test_stat = self.F

    def between_group_sum_of_squares(self):
        X_T = sum([self.ns[i]*self.means[i] for i in range(self.k)]) / float(self.N)
        SS_B = sum([self.ns[i]*(self.means[i] - X_T)**2 for i in range(self.k)])
        return SS_B

    def within_group_sum_of_squares(self):
        SS_W = sum( [(self.ns[i] - 1)*self.variances[i]**2 for i in range(self.k)] )
        return SS_W

    def between_group_mean_squares(self):
        MS_B = self.SS_B / float(self.k - 1)
        return MS_B

    def within_group_mean_squares(self):
        MS_W = self.SS_W / float(self.N - self.k)
        return MS_W

    def test_statistic(self):
        self.F = self.MS_W / self.MS_B

    def get_F(self):
        print(self.F)


class KruskalWallis(object):
    """ Compares three or more independent random sample mean ranks
    for difference.

    Requirements
    ------------
    1. Three or more (k) random samples.
    2. Each population has an underlying continuous distribution.
    3. Variable is measured at ordinal scale or downgraded from 
       interval/ratio scale to ordinal.

    Null Hypthothesis
    -----------------
    The populations from which the three or more (k) samples have been
    drawn are all identical.

    Test Statistic
    --------------

        H = { [ (12 / (N * (N + 1)) * sum(NumberObservationsInSample_i * MeanRankInSampl_i) ] -
              3 * (N + 1) } /
            [ 1 - sum(T) / (N^3 - N)]

        where

        N = TotalNumberObservationsInAllSamples

        T = NumberTiedObservations^3 - NumberTiedObservations

    """                         
    def __init__(self, rs):
        """
        Parameters
        ----------
        rs : array
            List of ranks of each sample.
        """
        self.rs = np.asarray(rs)
        self.k = len(rs)
        self.ns = np.array([len(rs[i]) for i in range(self.k)])
        self.N = float(sum(self.ns))
        self.H = None
        self.sum_n_r = None
        self.mean_rs = self.mean_rs()
        self.T = self.tie_correction()
        self.test_statistic()

    def tie_correction(self):
        num_tied_observations = len(self.mean_rs) - len(set(self.mean_rs))
        T = num_tied_observations**3 - num_tied_observations
        return T

    def mean_rs(self):
        rs = self.rs
        mean_rs = [np.array(rs[i]).mean() for i in range(self.k)]
        return mean_rs

    def test_statistic(self):
        N = self.N

        self.sum_n_r = sum([self.ns[i]*(self.mean_rs[i])**2 for i in range(self.k)])

        self.H = ( ( (12/(N*(N + 1))) * self.sum_n_r ) - 3*(N+1) ) / \
            float(1 - (self.T/(N**3 - N)))

    def get_H(self):
        print(self.H)


