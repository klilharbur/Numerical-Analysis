"""
In this assignment you should find the intersection points for two functions.
"""

import numpy as np
import time
import random
from collections.abc import Iterable



class Assignment2:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass

    def intersections(self, f1: callable, f2: callable, a: float, b: float, maxerr=0.001) -> Iterable:
        """
        Find as many intersection points as you can. The assignment will be
        tested on functions that have at least two intersection points, one
        with a positive x and one with a negative x.

        This function may not work correctly if there is infinite number of
        intersection points.


        Parameters
        ----------
        f1 : callable
            the first given function
        f2 : callable
            the second given function
        a : float
            beginning of the interpolation range.
        b : float
            end of the interpolation range.
        maxerr : float
            An upper bound on the difference between the
            function values at the approximate intersection points.


        Returns
        -------
        X : iterable of approximate intersection Xs such that for each x in X:
            |f1(x)-f2(x)|<=maxerr.

        """

        def compute_difference(f1, f2, points):
            return [f1(p) - f2(p) for p in points]

        def refine_interval(f1, f2, left, right, maxerr):
            iterations=0
            max_iter = 1000
            while  max_iter > iterations and abs(right - left) > maxerr  :
                mpoint = (left + right) / 2
                if (f1(left) - f2(left)) * (f1(mpoint) - f2(mpoint)) <= 0:
                    right = mpoint
                else:
                    left = mpoint
                iterations+=1
            return (left + right) / 2

        num_points = 1000
        points = np.linspace(a, b, num_points)
        diff = compute_difference(f1, f2, points)
        x = []

        for i in range(len(points) - 1):
            if abs(diff[i]) <= maxerr or abs(diff[i + 1]) <= maxerr or diff[i] * diff[i + 1] < 0:
                sub_points = np.linspace(points[i], points[i + 1], 100)
                sub_diff = compute_difference(f1, f2, sub_points)

                for j in range(len(sub_points) - 1):
                    if abs(sub_diff[j]) <= maxerr or abs(sub_diff[j + 1]) <= maxerr or sub_diff[j] * sub_diff[j + 1] < 0:
                        mpoint = refine_interval(f1, f2, sub_points[j], sub_points[j + 1], maxerr)
                        if abs(f1(mpoint) - f2(mpoint)) <= maxerr:
                            if not x or abs(mpoint - x[-1]) > 0.01:
                                x.append(mpoint)

        return x


##########################################################################


import unittest
from sampleFunctions import *
from tqdm import tqdm
from commons import f2_noise, f3_noise


class TestAssignment2(unittest.TestCase):

    def setUp(self):
        self.ass2 = Assignment2()

    def test_linear_functions(self):
        f1 = lambda x: 2 * x + 1
        f2 = lambda x: -x - 1

        X = self.ass2.intersections(f1, f2, -10, 10, maxerr=0.001)
        for x in X:
            self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))

    def test_polynomials(self):
        f1, f2 = randomIntersectingPolynomials(10)
        X = self.ass2.intersections(f1, f2, -1, 1, maxerr=0.001)
        for x in X:
            self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))

    def test_sinusoidal_functions(self):
        f1 = sinus()
        f2 = lambda x: 0.5 * np.sin(2 * x)
        X = self.ass2.intersections(f1, f2, -10, 10, maxerr=0.001)
        for x in X:
            self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))

    def test_strong_oscillations(self):
        f1 = strong_oscilations()
        f2 = lambda x: 0
        X = self.ass2.intersections(f1, f2, 0.01, 1, maxerr=0.001)
        for x in X:
            self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))

    def test_noisy_functions(self):
        X = self.ass2.intersections(f2_noise, f3_noise, -1, 1, maxerr=0.01)
        for x in X:
            self.assertGreaterEqual(0.01, abs(f2_noise(x) - f3_noise(x)))


if __name__ == "__main__":
    unittest.main()
