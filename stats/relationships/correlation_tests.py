""" Correlation tests.

Author:
    
    C.M. Gosmeyer

Date:

    Apr 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe

"""

import numpy as np

class PearsonCorrelation(object):
    """ Determines if an association exists between two variables.

    Requirements
    ------------
    1. Randaom sample of paired variables.
    2. Variables have a linear association.
    3. Variables are measured at interval or ratio scale.
    4. Variables are bivariate normally distributed.

    Null Hypthothesis
    -----------------
    H0 : PopulationCorrelationCoefficient = 0 
        No correlation exists in the populations of the two variables.

    Test Statistic
    --------------

        t = SampleCorrelationCoefficient / StandardErrorCorrelationEstimate

    where

        StandardErrorCorrelationEstimate =  sqrt(1 - SampleCorrelationCoefficient^2) / sqrt(NumberPairs - 2)
    """
    def __init__(self, xs=[], ys=[], Z_x=None, Z_y=None):
        """
        Parameters
        ----------
        xs : array
            The X values.
        ys : array
            The Y values.
        Z_x : array
            [Optional in place of 'xs'] The Z-scores of X variable.
        Z_y : array
            [Optional in place of 'ys'] The Z-score of Y variable.
        """
        self.xs = np.asarray(xs)
        self.ys = np.asarray(ys)
        self.Z_x = Z_x
        self.Z_y = Z_y
        self.n = len(self.xs)

        self.t = None
        self.r = self.correlation_coefficient()
        self.standard_error = self.standard_error()
        self.test_statistic()
        self.test_stat = self.t

    def correlation_coefficient(self):
        if Z_x != None and Z_y != None:
            r = sum( [self.Z_x[i]*self.Z_x[i] for i in range(len(self.Z_x))] ) / len(self.Z_x)
        else:
            sum_xy = sum( [self.xs[i]*self.ys[i] for i in range(self.n)] )
            sum_x = sum( [self.xs[i] for i in range(self.n)] )
            sum_y = sum( [self.ys[i] for i in range(self.n)] )
            sum_x2 = sum( [self.xs[i]**2 for i in range(self.n)] )
            sum_y2 = sum( [self.ys[i]**2 for i in range(self.n)] )
            r = (sum_xy - (sum_x*sum_y / float(self.n))) / \
                (np.sqrt(sum_x2-((sum_x)**2/float(self.n)))*np.sqrt(sum_y2-((sum_y)**2/float(self.n))))

        return r

    def standard_error(self):
        standard_error = np.sqrt((1-self.r**2)/(float(self.n)-2.))
        return standard_error

    def test_statistic(self):
        self.t = self.r / self.standard_error

class SpearmanRankCorrelation(object):
    """ Determines if an association exists between two variables.

    Requirements
    ------------
    1. Randaom sample of paired variables.
    2. Variables have a monotonically increasing or decreasing 
       association.
    3. Variables are measured at ordinal scale or downgraded from
       interval/ratio to ordinal.

    Null Hypthothesis
    -----------------
    H0 : PopulationCorrelationCoefficient = 0
        No relationship exists between the two variables in the 
        population.

    Test Statistic
    --------------

        Z_rs = SampleCorrelationCoefficient * sqrt(NumberPairedValues - 1)

        where

        SampleCorrelationCoefficient = 1 - (6*(sum(DifferenceInRanksOfVariables)) / 
                                            (NumberPairedValues^3 - NumberPairedValues))

    Notes
    -----
    1. Assumption that using Z distribution.
    2. Assumption that the number of rank ties does not exceed 25% of data.
    """
    def __init__(self, x_ranks, y_ranks):
        """
        Parameters
        ----------
        x_ranks : array
            Ranks of the X variable.
        y_ranks : array
            Ranks of the Y variable.
        """
        self.x_ranks = x_ranks
        self.y_ranks = y_ranks
        self.n = len(x_ranks)
        
        self.Z_rs = None
        rs = self.correlation_coefficient()
        self.test_statistic()
        self.test_stat = self.Z_rs

    def correlation_coefficient(self):
        sum_diffs = sum( [(self.x_ranks[i]-self.y_ranks[i])**2 for i in range(self.n)] )
        rs = 1.0 - ((6*sum_diffs) / (self.n**3 - self.n))
        return rs

    def test_statistic(self):
        self.Z_rs = self.rs * np.sqrt(self.n - 1.0)

