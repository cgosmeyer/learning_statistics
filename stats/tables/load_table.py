""" 

Author:
    
    C.M. Gosmeyer

Date:

    Mar 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe

To Do:

    Should tables interpolate?

"""

import numpy as np
import pandas as pd

class LoadTable(object):
    """
    """
    def __init__(self, filename):
        self.filename = filename

    def load_table(self):
        table = pd.read_csv(self.filename)
        return table

class LoadNormalTable(LoadTable):
    """ A normal table object.
    """
    def __init__(self):
        LoadTable.__init__(self, 'normal_table.csv')
        temp_table = self.load_table()
        self.normal_table = temp_table.set_index("z")

    def find_z(self, prob):
        """ Given probability, return nearest Z-score from normal table.

        Parameters
        ----------
        prob : float
            The probability, i.e., the area under section of probability
            distriubtion curve.

        Returns
        -------
        z_score : float
            The Z-score or standard score.
        """
        normal_table = self.normal_table

        # Find closest probability in table
        nearest_probs = []
        for col in list(normal_table):
            nearest_probs.append(find_nearest(normal_table[col], prob))
        nearest_probs = np.asarray(nearest_probs)
        final_prob = find_nearest(nearest_probs, prob)

        # Return the column and row
        for col in list(normal_table):
            if final_prob in list(normal_table[col]):
                z1 = col

        for i in normal_table.index:
            if final_prob == normal_table[z1][i]:
                z0 = i
        
        # Build Z-score
        z_score = float(z0) + float(z1)  

        return z_score

    def find_prob(self, z):
        """ Given Z-score, return nearest probability from table.

        Parameters
        ----------
        z_score : float
            The Z-score or standard score.

        Returns
        -------
        prob : float
            The probability, i.e., the area under section of probability
            distriubtion curve.
        """
        normal_table = self.normal_table

        z0 = round(z, 1)
        z1 = str(round(z, 2) - z0)

        prob = round(normal_table[z1][z0], 6)

        return prob

class LoadStudentsTTable(LoadTable):
    """ A normal table object.
    """
    def __init__(self, tails):
        """

        Parameters
        ----------
        tails : int
            1 or 2.
        """
        if tails == 1:
            LoadTable.__init__(self, 'students_t_table_one_tail.csv')
        else:
            LoadTable.__init__(self, 'students_t_table_two_tail.csv')
        temp_table = self.load_table()
        self.t_table = temp_table.set_index("df")

    def find_t(self, df, confidence=0.95):
        """  Finds the T-value of distribution.

        By default the confidence level is 95%.

        Parameters
        ----------
        df : int
            Degrees of freedom (size of sample).
        confidence : float
            The confidence level (area under distriubtion curve within
            interval). 

        Returns
        -------
        t_score : float
            The test statistic.
        """
        t_table = self.t_table
        neareset_confidence = find_nearest
        t_score = t_table[str(nearest_confidence)][df]

        return t_score

    def find_confidence(self, t, df):
        """ Finds confidence level (area) of tail(s) of distribution.

        Parameters
        ----------
        t : float
            The test statistic.
        df : int
            Degrees of freedom (size of sample).       
        """


def find_nearest(array, value):
    idx = pd.Series((np.abs(array-value))).idxmin()
    return array[idx]
