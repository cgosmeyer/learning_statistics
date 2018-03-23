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

def find_nearest(array, value):
    idx = pd.Series((np.abs(array-value))).idxmin()
    return array[idx]

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
