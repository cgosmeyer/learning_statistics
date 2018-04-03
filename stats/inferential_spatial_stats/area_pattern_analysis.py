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
        self.sum_links = self.J * 2

        self.expected_joins = self.expected_joins()
        self.sigma_expected_joins = self.sigma_expected_joins()
        self.Z_b = None 
        self.test_statistic()
        self.test_stat = self.Z_b

    def expected_joins(self):
        B = self.B
        W = self.W
        J = self.J
        N = self.N
        expected_joins = 2*J*B*W / (N*(N-1))

        return expected_joins

    def sigma_expected_join(self):
        B = self.B
        W = self.W
        J = self.J
        N = self.N
        sum_links = self.sum_links
        link_list_sub_1 = sum([ L-1 for L in self.link_list ])

        sigma_expected_joins = np.sqrt( self.expected_joins +
            (sum_L*link_list_sub_1*B*W / (N*(N-1))) +
            ((4*(J*(J-1)-sum_links*link_list_sub_1)*B*(B-1)*W*(W-1)) / (N*(N-1)*(N-2)*(N-3))) -
            self.expected_joins**2 )

        return sigma_expected_joins       

    def test_statistic(self): 
        self.Z_b = (self.observed_joins - self.expected_joins) / self.sigma_expected_joins

    def get_Zb(self):
        print(self.Z_b)



