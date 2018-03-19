""" Two-sample difference tests.

Author:
    
    C.M. Gosmeyer

Date:

    Mar 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe

"""

import numpy as np

class DiffOfMeans(object):
    """ Base class for two-sample difference of means tests.
    """
    def __init__(self, n1, n2):

        """
        Parameters
        ----------
        n1 : int
            Size of sample 1.
        n2 : int
            Size of sample 2.
        """

        self.n1 = float(n1)
        self.n2 = float(n2)
        self.test_stat = None

    def get_test_stat(self):
        print(self.test_stat)


class ZTest(DiffOfMeans):
    """ Compares two independent random sample means for difference.

    Requirements
    ------------
    1. Two independent random samples.
    2. Each population normally distributed. (i.e., follows Z 
       distribution)
    3. Variable is measured at interval or ratio scale.

    Null Hypthothesis
    -----------------
    population mean 1 = population mean 2

    Test Statistic
    --------------

        1. If SampleSize >= 30 and variances of both populations known:

        Z = SampleMean1 - SampleMean2 / StandardErrorOfDifferenceOfMeans

        where

        StandardErrorOfDifferenceOfMeans = sqrt( (StandErr1^2 / NumberSamples1) +
                                                 (StandErr2^2 / NumberSamples2) )


        2. If SampleSize < 30 and variances of populations *unknown* but assumed *equal*:

        t = SampleMean1 - SampleMean2 / StandardErrorOfDifferenceOfMeans

        where
        
        StandardErrorOfDifferenceOfMeans = PVE * sqrt( (1 / NumberSamples1) +
                                                       (1 / NumberSamples2) )

        where

        PVE = sqrt( [SampleVariance1^2 * (NumberSamples1 - 1) + 
                     SampleVariance2^2 * (NumberSamples2 - 1)] \
                    [NumberSamples1 + NumberSamples2 - 2] )
        

        3. If SampleSize < 30 and variances of populations *unknown* but 
        assumed *unequal*:

        SVE = StandardErrorOfDifferenceOfMeans 
            = sqrt( (SampleVariance1^2 / NumberSamples1) +
                    (SampleVariance2^2 / NumberSamples2) )
    """
    def __init__(self, n1, n2, mean1, mean2, s1, s2, sigma1=None, sigma2=None):
        DiffOfMeans.__init__(self, n1, n2)
        """
        Parameters
        ----------
        mean1 : float
            Mean of sample 1.
        mean2 : float
            Mean of sample 2.
        s1 : float
            Variance of sample 1.
        s2 : float
            Variance of sample 2.
        sigma1 : float
            Variance of population 1, if known.
        sigma2 : float
            Variance of population 2, if known.
        """
        self.mean1 = mean1
        self.mean2 = mean2
        self.s1 = s1
        self.s2 = s2
        self.sigma1 = sigma1
        self.sigma2 = sigma2
        self.Z = None
        self.t = None
        self.sigma_x1subx2 = None
        self.test_stat = None
        self.test_statistic()
    
    def standard_error(self, var1, var2):
        """ Calculates standard error of difference of means.
        """
        if self.sigma1 != None and self.sigma2 != None:
            sigma_x1subx2 = np.sqrt( (var1**2 / self.n1) + (var2**2 / self.n2) )

        elif var1 == var2:
            PVE = np.sqrt( (var1**2 * (self.n1 - 1) + var2**2 * (n2 - 1)) / \
                            (self.n1 + self.n2 - 2) )
            sigma_x1subx2 = PVE * np.sqrt( (1 / self.n1) + (1 / self.n2) )

        elif var1 != var2:
            SVE = np.sqrt( (var1**2 / self.n1) + (var2**2 / self.n2) )
            sigma_x1subx2 = SVE

        return sigma_x1subx2

    def test_statistic(self):
        """ Calculates test statistic.

        Should it return whether used Z or t?
        """
        if self.sigma1 != None and self.sigma2 != None and self.n1 >= 30 and self.n2 >= 30:
            sigma_x1subx2 = self.standard_error(self.sigma1, self.sigma2)
            self.Z = (self.mean1 - self.mean2) / sigma_x1subx2
            self.test_stat = self.Z

        elif (self.sigma1 != None or self.sigma2 != None) or (self.n1 < 30 or self.n2 < 30):
            sigma_x1subx2 = self.standard_error(self.s1, self.s2)
            self.t = (self.mean1 - self.mean2) / sigma_x1subx2
            self.test_stat = self.t

        self.sigma_x1subx2 = sigma_x1subx2

    def get_Z(self):
        print(self.Z)

    def get_t(self):
        print(self.t)

class WilcoxonRankSum(DiffOfMeans):
    """ Compares two independent random sample rank sums for difference
    using Wilcoxon rank sum "W" test.

    Requirements
    ------------
    1. Two independent random samples.
    2. Both population distributions have the same shape (but not
       necessarily normal).
    3. Variable is measured at ordinal or downgraded from interval/raio
       scale to ordinal.

    Null Hypthothesis
    -----------------
    Distribution of measurements for the first population is equal to 
    that of the second population.

    Test Statistic
    --------------
    
        Z_w = SumOfRanksSample_i - MeanRankOfW_i / StandardDeviationOfW

        where

        MeanRankOfW_i = SampleSize_i * ([SampleSize1 + SampleSize2 + 1] / 2)

        and

        StandardDeviationOfW = sqrt( SampleSize1 * SampleSize2 * 
                                    {[SampleSize1 + SampleSize2 + 1] / 12} )

        "W" is the Zw of the group with the *smaller* sample size.

    """
    def __init__(self, n1, n2, W1, W2):
        DiffOfMeans.__init__(self, n1, n2)
        """
        Parameters
        ----------
        W1 : float
            The sum of ranks for sample 1.
        W2 : float
            The sum of ranks for sample 2.
        """
        self.W1 = W1
        self.W2 = W2
        self.Zw = None
        self.s_w = self.standard_deviation()
        self.test_statistic()
        self.test_stat = self.Zw

    def standard_deviation(self):
        s_w = np.sqrt( self.n1 * self.n2 * (self.n1 + self.n2 + 1) / 12.0 )
        return s_w
    
    def mean_rank_W(self, n):
        mean_rank_W = n * (self.n1 + self.n2 + 1) / 2.0
        return mean_rank_W

    def test_statistic(self):
        # Calculate for the sample with smaller size.
        if self.n1 < self.n2:
            self.Zw = (self.W1 - self.mean_rank_W(self.n1)) / self.s_w
        else:
            self.Zw = (self.W2 - self.mean_rank_W(self.n2)) / self.s_w

    def get_Zw(self):
        print(self.Zw)


class DiffOfProportions():
    """ Compares two independent random sample proportions for difference.

    Requirements
    ------------
    1. Two independent random samples.
    2. Variable is organized by dichotomous (binary) categories.

    Null Hypthothesis
    -----------------
    Proportion1 = Proportion2

    Test Statistic
    --------------

        Z_p = (SampleProportion1 - SampleProportion2) / StandErrorDifferenceOfProportions

        where

        StandErrorDifferenceOfProportions = sqrt( PooledEstimate * (1 - PooledEstimate ) * 
                                                 ( [SampleSize1 + SampleSize1] 
                                                   / SampleSize1 * SampleSize2 ) )

        where

        PooledEstimate = (SampleSize1 * SampleProportion1 + SampleSize2 * SampleProportion2) / 
                         (SampleSize1 + SampleSize2)
    """
    def __init__(self, n1, n2, p1, p2):
        """
        Parameters
        ----------
        n1 : int
            Size of sample 1.
        n2 : int
            Size of sample 2.
        p1 : int
            Proportion of sample 1 in category of focus.
        p2 : int
            Proportion of sample 2 in category of focus. 
        """
        self.n1 = float(n1)
        self.n2 = float(n2)
        self.p1 = p1
        self.p2 = p2
        self.pooled_estimate = None
        self.Zp = None
        self.sigma_p1subp2 = self.standard_error()
        self.test_statistic()
        self.test_stat = self.Zp

    def standard_error(self):
        """ Calculates standard error of difference of proportions.
        """
        # The weighted proportion of the two samples.
        pooled_estimate = (self.n1 * self.p1 + self.n2 * self.p2) / (self.n1 + self.n2)
        sigma_p1subp2 = np.sqrt( pooled_estimate * (1 - pooled_estimate) * \
                                 ((self.n1 + self.n2) / (self.n1 * self.n2)) )
        self.pooled_estimate = pooled_estimate
        return sigma_p1subp2

    def test_statistic(self):
        self.Zp = abs(self.p1 - self.p2) / self.sigma_p1subp2

    def get_Zp(self):
        print(self.Zp) 

