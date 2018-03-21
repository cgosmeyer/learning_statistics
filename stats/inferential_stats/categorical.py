""" Categorical difference tests.

Author:
    
    C.M. Gosmeyer

Date:

    Mar 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe
"""

import numpy as np

class GoodnessOfFit(object):
    """ Base class for goodness-of-fit tests.
    """
    def __init__(self):

        """
        Parameters
        ----------
        """
        self.test_stat = None


class ChiSquare(GoodnessOfFit):
    """ Compares random sample frequency counts of a single variable with
    expected frequency counts (goodness-of-fit).

    Requirements
    ------------
    1. Single random sample.
    2. Variables are organized by nominal or ordinal categories; frequency
       counts by category are input to statistical test.
    3. If two categories, both expected frequency counts must be at least
       five. If three or more categories, no more than 1/5 of the expected
       frequency counts should be less than five, and no expected frequency
       count should be less than two.

    Null Hypthothesis
    -----------------
    Population from qhich sample has been drawn fits an expected
    frequency distribution; no difference between observed and expected
    frequencies.

    Test Statistic
    --------------

        Chi^2 = sum( ObservedFrequencyCountInCategory_i - ExpectedFrequencyCountInCategory_i) /
                    ExpectedFrequencyCountInCategory_i )
    """                         
    def __init__(self, FC_o, FC_e):
        GoodnessOfFit.__init__(self)
        """
        Parameters
        ----------  
        FC_o : array
            Frequency counts in each category of the observed distribution.
        FC_e : array
            Frequency counts in each category of the expected distribution.
        """
        self.FC_o = np.asarray(FC_o)
        self.FC_e = np.asarray(FC_e)
        self.k = len(FC_o)
        self.chi_square = None
        self.test_statistic()
        self.test_stat = self.chi_square

    def test_statistic(self):
        self.chi_square = sum( [ ((self.FC_o[i] - self.FC_e[i])**2) / float(self.FC_e[i]) for i in range(self.k)] )


class KolmogorovSmirnov(GoodnessOfFit):
    """ Compares random sample frequency counts of a single variable with
    expected frequency counts (goodness-of-fit).

    Requirements
    ------------
    1. Single random sample.
    2. Population is continuously distributed (test less valid with 
       discrete population).
    3. Variable is measured at ordinal scale or downgraded from 
       interval/ratio to ordinal.

    Null Hypthothesis
    -----------------
    Population from qhich sample has been drawn fits an expected
    frequency distribution; no difference between observed and expected
    frequencies.

    Test Statistic
    --------------

        D = max( abs( CFR_o(X) - CFR_e(X) ) )

        where X is the variable

    To Do
    -----
    * should have built-in options of normal distribution
    * also ability to build a CFR?
    """                         
    def __init__(self, CFR_o, CFR_e):
        GoodnessOfFit.__init__(self)
        """
        Parameters
        ----------  
        CFR_o : array
            Observed cumulative relative frequencies for variable.
        CFR_e : array
            Expected cumulative relative frequencies for variable.
        """
        self.CFR_o = np.asarray(CFC_o)
        self.CFR_e = np.asarray(CFR_e)
        self.D = None
        self.test_statistic()
        self.test_stat = self.D

    def test_statistic(self):
        self.D = np.max( abs(self.CFR_o - self.CFR_e) )


class Contingency(object):
    """ Compares random sample frequency counts of two variables for
    statistical independence.

    Requirements
    ------------
    1. Single random sample.
    2. Variables are organized by nominal or ordinal categories; frequency
       counts by category are input to statistical test.
    3. No more than 1/5 of the expected frequency counts should be less 
       than five, and no expected frequency count should be less than two.

    Null Hypthothesis
    -----------------
    There is no relationship between two variables in teh population from
    which sample has been drawn.

    Test Statistic
    --------------

        Chi^2 = sum( ObservedFrequencyCountInRowCol_ij - ExpectedFrequencyCountInRowCol_ij) /
                    ExpectedFrequencyCountInRowCol_ij )
    """                         
    def __init__(self, FC_o):
        """
        Parameters
        ----------  
        FC_o : 2-D array
            Frequency counts in each row and column of contingency table.
        FC_e : 2-D array
            Frequency counts in each row and column of contingency table.

        Example
        -------
        FC_o = [[1,2,3], [4,5,6]], then k = 3 and r = 2
        """
        self.FC_o = np.asarray(FC_o)
        self.k = len(FC_o[0])
        self.r = len(FC_o)
        self.FC_e = self.expected_frequency_counts()
        self.chi_square = None
        self.test_statistic()
        self.test_stat = self.chi_square

    def expected_frequency_counts(self):
        FC_e = np.empty_like(self.FC_o)
        N = 0
        for i in range(self.k):
            for j in range(self.r):
                FC_e[i][j] = sum(self.FC_o[i]) * sum(self.FC_o.T[j])
            N += sum(self.FC_o[i])

        return FC_e / float(N)

    def test_statistic(self):
        chi_square = 0
        for i in range(self.k):
            for j in range(self.r):
                chi_square += ((self.FC_o[j][i] -  self.FC_e[j][i])**2 / float(self.FC_e[j][i]))

        self.chi_square = chi_square
