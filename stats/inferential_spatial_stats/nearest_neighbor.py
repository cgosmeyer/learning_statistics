""" Nearest-neighbor analysis.

Author:
    
    C.M. Gosmeyer

Date:

    Mar 2018

References:

    "Introduction to Statistical Problem Solving in Geography", 
    J.C. McGrew, Jr., A.J. Lembo, Jr., C.B. Monroe

"""

import numpy as np

class NearestNeighbor(object):
    """ Determine whether a random (Poisson) process has generated a point
    pattern.

    R = 2.149 (perfectly dispersed)
    R = 1.0 (random)
    R = 0.0 (perfectly clustered)

    where

    R = MeanNNDistance /  MeanPerfectlyRandomNNDistance

    Requirements
    ------------
    1. Randaom sample of points from a population.
    2. Sample points are independently selected.

    Null Hypthothesis
    -----------------
    mean NN distance = mean perfectly random NN distance (point pattern
        is random)

    Test Statistic
    --------------

        Z_n = (MeanNNDistance - MeanPerfectlyRandomNNDistance) / StandardErrorNN

        where

        StandardErrorNN = 0.26136 / sqrt( NumberPoints * Density )
    """                         
    def __init__(self, area, x_pos=[], y_pos=[], NND=None, n=None):
        """
        Parameters
        ----------  
        area : int
            The area of test region.
        x_pos : array
            The x-positions of points.
        y_pos : array
            The y-positions of points.
        NND : float
            Nearest neighbor density, if know already. 
        n : int
            Number of points. Only need to fill out if already know NND.
        """
        if NND == None:
            self.x_pos = np.asarray(x_pos)
            self.y_pos = np.asarray(y_pos)
            self.n = len(x_pos)
            self.NND = self.mean_nearest_neighbor()

        else:
            self.n = n
            self.NND = NND

        self.area = float(area)
        self.density = self.n / self.area
        self.NND_R = 1. / (2. * np.sqrt(self.density))  # Perfectly random sample
        self.R = self.NND / self.NND_R

        self.sigma_NND = None
        self.standard_error()
        self.Z_n = None
        self.test_statistic()

        self.test_stat = self.Z_n

    def mean_nearest_neighbor(self):
        NND = []
        
        # Find nerarest neighbor distances.
        for i1, j1 in zip(self.x_pos, self.y_pos):
            a = [np.sqrt((i1-i2)**2 + (j1-j2)**2) for i2, j2 in zip(self.x_pos, self.y_pos)]
            a = np.asarray(a)
            NND.append((min(a[a != 0])))

        np.asarray(NND)
        return np.mean(NND)
  
    def standard_error(self):
        self.sigma_NND = 0.26136 / np.sqrt(self.n * self.density)

    def test_statistic(self):
        self.Z_n = (self.NND - self.NND_R) / self.sigma_NND



