"""
In this assignment you should interpolate the given function.
"""

import numpy as np


from sampleFunctions import randomIntersectingPolynomials, sinus, strong_oscilations, bezier3


class Assignment1:



    def __init__(self):
        """
        Here goes any one time calculation that need to be made before
        starting to interpolate arbitrary functions.
        """

        pass

    def chebyshev_points(self, a, b, n):
        """
        Compute Chebyshev points for interpolation within the interval [a, b].
        """
        theta = np.linspace(np.pi, 0, n)
        points = 0.5 * (a + b) + 0.5 * (b - a) * np.cos(theta)
        return points



    def tridiagonal_solver(self, main_diag, l_diag, u_diag, rhs):
        """
        Solve a tridiagonal system of equations.
        """
        n = len(rhs)
        c_prime, d_prime = [0] * n, [0] * n

        c_prime[0] = u_diag[0] / main_diag[0]
        d_prime[0] = rhs[0] / main_diag[0]

        for i in range(1, n):
            m = main_diag[i] - l_diag[i] * c_prime[i - 1]
            c_prime[i] = u_diag[i] / m
            d_prime[i] = (rhs[i] - l_diag[i] * d_prime[i - 1]) / m

        x = [0] * n
        x[-1] = d_prime[-1]
        for i in range(n - 2, -1, -1):
            x[i] = d_prime[i] - c_prime[i] * x[i + 1]

        return x

    def binary_search(self, x, x_vals):
        """
        Efficient binary search to locate interval for interpolation.
        """
        left, right = 0, len(x_vals) - 2
        while left <= right:
            mid = (left + right) // 2
            if x_vals[mid] <= x <= x_vals[mid + 1]:
                return mid
            elif x < x_vals[mid]:
                right = mid - 1
            else:
                left = mid + 1
        return -1

    def polynomial_interpolation(self, x_points, y_points):
        """
        Efficient polynomial interpolation using Newton's Divided Differences (O(n)).
        """

        def divided_differences(x_points, y_points):
            """
            Calculate the divided differences table.
            """
            n = len(x_points)
            coef = np.copy(y_points)

            for j in range(1, n):
                coef[j:] = (coef[j:] - coef[j - 1:-1]) / (x_points[j:] - x_points[:-j])

            return coef

        coefficients = divided_differences(x_points, y_points)

        def newton_polynomial(x_value):
            """
            Evaluate the Newton polynomial at a given x_value.
            """
            n = len(coefficients)
            result = coefficients[-1]
            for i in range(n - 2, -1, -1):
                result = result * (x_value - x_points[i]) + coefficients[i]
            return result

        return newton_polynomial

    def interpolate(self, f: callable, a: float, b: float, n: int) -> callable:
        """
        Adaptive interpolation based on the function's behavior.
        """
        x_cheb = self.chebyshev_points(a, b, n)
        y_cheb = [f(x) for x in x_cheb]

        return self.polynomial_interpolation(x_cheb, y_cheb)



##########################################################################


import unittest
from functionUtils import *
from tqdm import tqdm


class TestAssignment1(unittest.TestCase):

    def test_with_poly(self):
        T = time.time()

        ass1 = Assignment1()
        mean_err = 0

        d = 30
        for i in tqdm(range(100)):
            a = np.random.randn(d)

            f = np.poly1d(a)

            ff = ass1.interpolate(f, -10, 10, 100)

            xs = np.random.random(200)
            err = 0
            for x in xs:
                yy = ff(x)
                y = f(x)
                err += abs(y - yy)

            err = err / 200
            mean_err += err
        mean_err = mean_err / 100

        T = time.time() - T
        print(T)
        print(mean_err)

    def test_with_poly_restrict(self):
        ass1 = Assignment1()
        a = np.random.randn(5)
        f = RESTRICT_INVOCATIONS(10)(np.poly1d(a))
        ff = ass1.interpolate(f, -10, 10, 10)
        xs = np.random.random(20)
        for x in xs:
            yy = ff(x)





if __name__ == "__main__":
    unittest.main()
