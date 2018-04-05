""" Area pattern analysis tests.

Author:
    
    C.M. Gosmeyer

Date:

    Apr 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe
"""

import numpy as np

class JointCountBinary(object):
    """ Determine whether a random process has generated a binary (two-
    category) area pattern.

    Requirements
    ------------
    1. Each area is assigned to one of two categories.
    2. Each pair of areas must be defined as either adjacent ("joined")
    or nonadjacent (not "joined") in a consistent manner.

    Null Hypthothesis
    -----------------
    H0 : ObservedNumberBlack-WhiteJoins = ExpectedNumberBlack-WhiteJoins
        (area pattern is random)
    HA : ObservedNumberBlack-WhiteJoins != ExpectedNumberBlack-WhiteJoins
        (area pattern is NOT random)
    HA : ObservedNumberBlack-WhiteJoins > ExpectedNumberBlack-WhiteJoins
        (area is more dispersed than random)
    HA : ObservedNumberBlack-WhiteJoins < ExpectedNumberBlack-WhiteJoins
        (area pattern is is more clustered than random)

    Test Statistic
    --------------

    Z_b = (ObservedNumberBlack-WhiteJoins - ExpectedNumberBlack-WhiteJoins) 
           / StandardErrorExpectedNumberBlack-WhiteJoins

    where

    ExpectedNumberBlack-WhiteJoins = 2*J*B*W / N*(N-1)

    where

    J = total number of joins
    B = number of black areas
    W = number of white areas
    N = total number of areas  = B + W

    and

    StandardErrorExpectedNumberBlack-WhiteJoins = sqrt( ExpectedNumberBlack-WhiteJoins +
        [ sum(L)*(L-1)*B*W) / N(N-1) ] +
        [ 4*{J*(J-1) - sum(L)*(L-1)}*B*(B-1)*W*(W-1) / N*(N-1)*(N-2)*(N-3) ] -
        ExpectedNumberBlack-WhiteJoins^2 )

    where

    L = list of links for each area
    sum(L) = total number of links = 2J
    """                         
    def __init__(self, B, W, J, link_list, observed_joins):
        """
        Parameters
        ----------
        B : int
            Number of black areas.
        W : int
            Number of white areas.
        J : int
            Total number of joins.
        link_list : list
            List of links for each area.
        observed_joins : int
            Observed number of black-white joins.
        """
        self.B = float(B)
        self.W = float(W)
        self.J = float(J)
        self.observed_joins = float(observed_joins)
        self.link_list = np.asarray(link_list)

        self.N = self.B + self.W 
        self.expected_joins = self.return_expected_joins()
        self.sigma_expected_joins = self.return_sigma_expected_joins()
        self.Z_b = None 
        self.test_statistic()
        self.test_stat = self.Z_b

    def return_expected_joins(self):
        B = self.B
        W = self.W
        J = self.J
        N = self.N
        expected_joins = 2*J*B*W / (N*(N-1))

        return expected_joins

    def return_sigma_expected_joins(self):
        B = self.B
        W = self.W
        J = self.J
        N = self.N
        L_sums = sum([ L*(L-1) for L in self.link_list ])

        sigma_expected_joins = np.sqrt( self.expected_joins +
            (L_sums*B*W / (N*(N-1))) +
            ((4*(J*(J-1)-L_sums)*B*(B-1)*W*(W-1)) / (N*(N-1)*(N-2)*(N-3))) -
            self.expected_joins**2 )

        return sigma_expected_joins       

    def test_statistic(self): 
        self.Z_b = (self.observed_joins - self.expected_joins) / self.sigma_expected_joins

    def get_Zb(self):
        print(self.Z_b)


class MoransIndexGlobal(object):
    """ Identify significant spatial patterns within a study area.

    Requirements
    ------------
    1. Minimum of 30 geographic features.
    2. Attribute values measures on an ordinal or interval/ratio scale.

    Null Hypthothesis
    -----------------
    H0 : Attribute values are randomly distributed across features in 
    study area.

    Test Statistic
    --------------

    I = n * sum( (x_i - x_mean)*(x_j - x_mean) ) / J * sum( x - x_mean)^2

    where

    n = number of objects
    J = number of joins
    x = area attribute value
    x_mean = mean of all area attribute values
    x_i, x_j = values of contiguous pairs

    Interpretation
    --------------

    Assuming significant p-value:

    I < 0 : observed pattern is dispersed
    I = 0 : observed pattern is random
    I > 0 : observed pattern is clustered

    """   
    def __init__(self, area_joins, area_attributes, assumption='normal'):
        """
        Parameters
        ----------
        area_joins : list of ints
            The number of joins for each area.
        area_attributes : list of lists
            The i, j area attributes for each join.
        assumption : str
            Either "normal" or "random"; will determine the calculated 
            variance of the distribution.
        """
        self.area_joins = np.asarray(area_joins) # L
        self.area_attributes = np.asarray(area_attributes) # x_i, x_j
        self.assumption = assumption

        self.n = float(len(area_joins))
        self.J = float(len(area_attributes))
        self.I = None
        self.test_statistic()
        self.test_stat = self.I
        self.var_I = self.variance()
        self.z_score = self.z_score()

    def test_statistic(self):
        xs = list(set([x[0] for x in self.area_attributes]))
        x_mean = np.mean(xs)
        x_sum_pairs = sum( [(x_i-x_mean)*(x_j-x_mean) for x_i, x_j in self.area_attributes] )
        x_variance_attribute_vals = sum( [(x-x_mean)**2 for x in xs] )
        self.I = (self.n * x_sum_pairs) / (self.J *  x_variance_attribute_vals)

    def variance(self):
        sum_L2 = float(sum(self.area_joins**2))
        if self.assumption == 'normal':
            var_I = (self.J*self.n**2 + 3*self.J**2 - self.n*sum_L2) / \
                    (self.J**2 * (self.n**2 - 1.))

        elif self.assumption == 'random':
            xs = list(set([x[0] for x in self.area_attributes]))
            x_mean = np.mean(xs)
            # Now calculate kurtosis.
            k = sum( [(x-x_mean)**4 for x in xs] ) / (len(xs) * np.std(xs)**4) - 3
            var_I = ( self.n * ( self.J*(self.n**2+3-3*self.n) + \
                               + 3*self.J**2 - self.n*sum_L2 ) - \
                      k * ( self.J*(self.n**2 - self.n) + \
                            6*self.J**2 - \
                            2*self.n*sum_L2 ) ) / \
                    ( self.J**2*(self.n-1)*(self.n-2)*(self.n-3) )

        else:
            var_I = 0

        return var_I

    def z_score(self):
        expected_I = -1. / (self.n - 1.)
        z_score = (self.I - expected_I) / np.sqrt(self.var_I)
        return z_score
