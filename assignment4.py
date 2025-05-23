"""
In this assignment you should fit a model function of your choice to data 
that you sample from a given function. 

The sampled data is very noisy so you should minimize the mean least squares 
between the model you fit and the data points you sample.  

During the testing of this assignment running time will be constrained. You
receive the maximal running time as an argument for the fitting method. You 
must make sure that the fitting function returns at most 5 seconds after the 
allowed running time elapses. If you take an iterative approach and know that 
your iterations may take more than 1-2 seconds break out of any optimization 
loops you have ahead of time.

Note: You are NOT allowed to use any numeric optimization libraries and tools 
for solving this assignment. 

"""

import numpy as np
import time
import random


class Assignment4:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass


    def fit(self, f: callable, a: float, b: float, d:int, maxtime: float) -> callable:
        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape.

        Parameters
        ----------
        f : callable.
            A function which returns an approximate (noisy) Y value given X.
        a: float
            Start of the fitting range
        b: float
            End of the fitting range
        d: int
            The expected degree of a polynomial matching f
        maxtime : float
            This function returns after at most maxtime seconds.

        Returns
        -------
        a function:float->float that fits f between a and b
        """

        # replace these lines with your solution

        start_time = time.time()
        is_exponential = self.detect_exponential(f, a, b)

        numOfSegments = 5
        segmentEdges = np.linspace(a, b, numOfSegments + 1)
        piecewise_poly = []

        for i in range(numOfSegments):
            if time.time() - start_time > maxtime:
                break

            start = segmentEdges[i]
            end = segmentEdges[i + 1]

            samples = 50000
            x_points = np.linspace(start, end, samples)

            if is_exponential:
                y_points = np.log(np.abs([f(x) + 1e-6 for x in x_points]))
            else:
                y_points = np.array([f(x) for x in x_points])

            A = np.vstack([x_points ** j for j in range(d + 1)]).T
            ATA = A.T @ A
            ATy = A.T @ y_points

            coeff = self.gaussJordan(ATA, ATy)
            piecewise_poly.append((start, end, coeff))

        def piecewise_function(x):
            for start, end, coeff in piecewise_poly:
                if start <= x <= end:
                    result = sum(c * (x ** i) for i, c in enumerate(coeff))
                    return np.exp(result) if is_exponential else result
            return 0

        return piecewise_function

    def detect_exponential(self, f, a, b, maxDiff=1000):

        test_x = np.linspace(a, b, 50)
        test_y = [f(x) for x in test_x]
        diff_y = np.diff(test_y)

        return np.any(np.abs(diff_y) > maxDiff)

    def gaussJordan(self, A, b):

        lenMat = len(b)
        mat = np.hstack((A, b.reshape(-1, 1)))
        for i in range(lenMat):
            mat[i] = mat[i] / mat[i, i]

            for j in range(lenMat):
                if i != j:
                    mat[j] = mat[j] - mat[j, i] * mat[i]

        return mat[:, -1]

##########################################################################


import unittest
from sampleFunctions import *
from tqdm import tqdm


class TestAssignment4(unittest.TestCase):

    def test_return(self):
        f = NOISY(0.01)(poly(1,1,1))
        ass4 = Assignment4()
        T = time.time()
        shape = ass4.fit(f=f, a=0, b=1, d=10, maxtime=5)
        T = time.time() - T
        self.assertLessEqual(T, 5)

    def test_delay(self):
        f = DELAYED(7)(NOISY(0.01)(poly(1,1,1)))

        ass4 = Assignment4()
        T = time.time()
        shape = ass4.fit(f=f, a=0, b=1, d=10, maxtime=5)
        T = time.time() - T
        self.assertGreaterEqual(T, 5)

    def test_err(self):
        f = poly(1,1,1)
        nf = NOISY(1)(f)
        ass4 = Assignment4()
        T = time.time()
        ff = ass4.fit(f=nf, a=0, b=1, d=10, maxtime=5)
        T = time.time() - T
        mse=0
        for x in np.linspace(0,1,1000):            
            self.assertNotEquals(f(x), nf(x))
            mse+= (f(x)-ff(x))**2
        mse = mse/1000
        print(mse)

        
        



if __name__ == "__main__":
    unittest.main()
