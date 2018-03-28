""" Quadrant analysis.

Author:
    
    C.M. Gosmeyer

Date:

    Mar 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe

Notes:

    I'm skeptipical about the rigor of quadrant analysis. Seems rather subjective:
    resize the grid until you like what you see. Even book says:

    "...more research needs to be conducted on optimal quadrant size..."
"""

import numpy as np

class Quadrant(object):
    """ Determine whether a random (Poisson) process has generated a
    point pattern.

    Requirements
    ------------
    1. Randaom sample of points from a population.
    2. Sample points are independently selected.

    Null Hypthothesis
    -----------------
    VMR = 1 (point pattern is random)

    Test Statistic
    --------------

        Chi-Square = VMR*(m - 1)

        where 

        VMR = Variance / Mean

        m = NumberOfCells

    Notes:

        What is df in this case? The total number of points or 
        the number of cells?
    """
    def __init__(self, x, f):
        """
        Parameters
        ----------
        x : array
            Number of points per cell.
        f : array
            Number of cells.
        """
        self.x = np.asarray(x)
        self.f = np.asarray(f) 
        self.n = float(sum(self.x)) # Number of points
        self.m = float(sum(self.f)) # Number of cells
        self.k = len(self.x) # Number of samples
        self.var = self.variance()
        self.mean = sum(self.x * self.f) / self.m
        self.chi_square = None
        self.test_statistic()
        self.test_stat = self.chi_square

    def variance(self):
        var = (sum([self.f[i]*self.x[i]**2 for i in range(self.k)]) - \
               (sum([(self.f[i]*self.x[i]) for i in range(self.k)])**2 / self.m)) / \
              (self.m - 1.0)
        return var

    def test_statistic(self):
        self.chi_square = (self.var / self.mean) * (self.m - 1.0)

