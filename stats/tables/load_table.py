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

    y = y1 + ((x - x1) / (x2 - x1)) * (y2 - y1)

"""

import numpy as np
import pandas as pd
import os

# Get absolute path to table files.
p = os.path.abspath(__file__)
p = '/'.join(p.split('/')[:-1])

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
        LoadTable.__init__(self, os.path.join(p, 'normal_table.csv'))
        temp_table = self.load_table()
        self.normal_table = temp_table.set_index("z")

    def find_z(self, prob, tails=1):
        """ Given probability, return nearest Z-score from normal table.

        Parameters
        ----------
        prob : float
            The probability, i.e., the area under section of probability
            distriubtion curve.
        tails : int
            1 or 2. The prob will be divided by this number (all 
            calculations assume one tail). Do not change to 2 if your
            `prob` value already is divided in half.

        Returns
        -------
        z_score : float
            The Z-score or standard score.
        """
        prob /= float(tails)
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

    def find_prob(self, z, tails=1):
        """ Given Z-score, return nearest probability from table.

        Parameters
        ----------
        z : float
            The Z-score or standard score.
        tails : int
            1 or 2.

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
        prob *= tails

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
            LoadTable.__init__(self, os.path.join(p, 'students_t_table_one_tail.csv'))
        else:
            LoadTable.__init__(self, os.path.join(p, 'students_t_table_two_tail.csv'))
        temp_table = self.load_table()
        self.t_table = temp_table.set_index("df")

    def find_t(self, df, confidence=0.95):
        """  Finds the T-value of distribution. The table goes to df-1000,
        after which all is effectively infinity and returns same value.

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
        nearest_confidence = round(find_nearest(list(t_table), 1.0-confidence), 4)
        nearest_df = round(find_nearest(t_table.index, df), 0)
        t_score = round(t_table[str(nearest_confidence)][nearest_df], 4)

        return t_score

    def find_confidence(self, t, df):
        """ Finds confidence level (area) of ONE tail of distribution.

        Parameters
        ----------
        t : float
            The test statistic.
        df : int
            Degrees of freedom (size of sample).       
        """
        t_table = self.t_table
        nearest_df = round(find_nearest(t_table.index, df), 0)
        nearest_t = round(find_nearest(t_table.loc[nearest_df], t), 6)
        for col in list(t_table):
            if nearest_t == round(t_table[col][nearest_df], 6):
                # Subtract from one to get confidence, divide by two to get
                # single section on positive side of distribution.
                confidence = (1.0 - float(col)) / 2.0
                return confidence

class LoadChi2Table(LoadTable):
    """ A normal table object.
    """
    def __init__(self):
        """
        """
        LoadTable.__init__(self, os.path.join(p, 'chi_square_table.csv'))
        temp_table = self.load_table()
        self.chi2_table = temp_table.set_index("df")  

    def find_chi2(self, df, confidence=0.95):
        """  Finds the T-value of distribution. The table goes to df-1000,
        after which all is effectively infinity and returns same value.

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
        chi2 : float
            The test statistic.
        """
        chi2_table = self.chi2_table
        nearest_confidence = round(find_nearest(list(chi2_table), 1.0-confidence), 4)
        nearest_df = round(find_nearest(chi2_table.index, df), 0)
        chi2 = round(chi2_table[str(nearest_confidence)][nearest_df], 4)
        return chi2

    def find_confidence(self, chi2, df):
        """ Finds confidence level (area) of right-hand-side of distribution.

        Parameters
        ----------
        chi2 : float
            The test statistic.
        df : int
            Degrees of freedom (size of sample).
        """
        chi2_table = self.chi2_table
        nearest_df = round(find_nearest(chi2_table.index, df), 0)
        nearest_chi2 = round(find_nearest(chi2_table.loc[nearest_df], chi2), 6)
        for col in list(chi2_table):
            if nearest_chi2 == round(chi2_table[col][nearest_df], 6):
                # Subtract from one to get confidence.
                confidence = (1.0 - float(col))
                return confidence

def find_nearest(array, value):
    array = np.array(array, dtype=float)
    value = float(value)
    idx = pd.Series((np.abs(array-value))).idxmin()
    return array[idx]
