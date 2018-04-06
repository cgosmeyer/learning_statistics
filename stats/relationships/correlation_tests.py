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

        self.t = None
        self.r = self.correlation_coefficient()

    def correlation_coefficient(self):
        if Z_x != None and Z_y != None:
            r = sum( [self.Z_x[i]*self.Z_x[i] for i in range(len(self.Z_x))] ) / len(self.Z_x)
        else:
            sum_xy = sum()
            sum_x =
            sum_y =
            sum_x2 =
            sum_y2 =  
            r = 

        return r

    def test_statistic(self):
        



    
