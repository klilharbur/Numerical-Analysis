"""
In this assignment you should find the area enclosed between the two given functions.
The rightmost and the leftmost x values for the integration are the rightmost and
the leftmost intersection points of the two functions.

The functions for the numeric answers are specified in MOODLE.


This assignment is more complicated than Assignment1 and Assignment2 because:
    1. You should work with float32 precision only (in all calculations) and minimize the floating point errors.
    2. You have the freedom to choose how to calculate the area between the two functions.
    3. The functions may intersect multiple times. Here is an example:
        https://www.wolframalpha.com/input/?i=area+between+the+curves+y%3D1-2x%5E2%2Bx%5E3+and+y%3Dx
    4. Some of the functions are hard to integrate accurately.
       You should explain why in one of the theoretical questions in MOODLE.

"""

import numpy as np
import time
import random
import assignment2


class Assignment3:
    def simpson3points(self, a, b, fa, fb, fm):
        return (b - a) * (fa + 4.0 * fm + fb) / 6.0

    def simpsonsRec(self, f, a, b, fa, fb, fm, S_ab, maxErr, callsLeft):
        if callsLeft < 2:
            return S_ab, 0

        m = 0.5 * (a + b)
        m1 = 0.5 * (a + m)
        m2 = 0.5 * (m + b)

        calls_used = 0
        if m1 not in self.memo and len(self.memo) < self.n:
            self.memo[m1] = f(m1)
            calls_used += 1
        fm1 = self.memo.get(m1, f(m1))

        if m2 not in self.memo and len(self.memo) < self.n:
            self.memo[m2] = f(m2)
            calls_used += 1
        fm2 = self.memo.get(m2, f(m2))

        S1 = self.simpson3points(a, m, fa, fm, fm1)
        S2 = self.simpson3points(m, b, fm, fb, fm2)

        error = abs(((S1 + S2) - S_ab)/(S1 + S2))
        if error < maxErr:
            return (S1 + S2), calls_used
        else:
            half_tol = 0.5 * maxErr
            calls_for_each_side = max(1, (callsLeft - calls_used) // 2)

            left_val, used_left = self.simpsonsRec(f, a, m, fa, fm, fm1, S1, half_tol, calls_for_each_side)
            right_val, used_right = self.simpsonsRec(f, m, b, fm, fb, fm2, S2, half_tol, calls_for_each_side)

            total_used = calls_used + used_left + used_right
            return (left_val + right_val), total_used



    def integrate(self, f, a, b, n) -> np.float32:
        if a == b:
            return np.float32(0.0)


        self.memo = {}
        self.n = n

        def F(x):
            if x not in self.memo and len(self.memo) < self.n:
                    self.memo[x] = f(x)
            return self.memo[x]

        fa = F(a)
        fb = F(b)
        m = 0.5 * (a + b)
        fm = F(m)

        S_ab = self.simpson3points(a, b, fa, fb, fm)
        callsUsed = len(self.memo)
        callsLeft = max(0, n - callsUsed)

        val, used = self.simpsonsRec(F, a, b, fa, fb, fm, S_ab, 0.0001, callsLeft)
        return np.float32(val)

    def areabetween(self, f1: callable, f2: callable) -> np.float32:
        """
        Finds the area enclosed between two functions. This method finds
        all intersection points between the two functions to work correctly.

        Example: https://www.wolframalpha.com/input/?i=area+between+the+curves+y%3D1-2x%5E2%2Bx%5E3+and+y%3Dx

        Note, there is no such thing as negative area.


        In order to find the enclosed area the given functions must intersect
        in at least two points. If the functions do not intersect or intersect
        in less than two points this function returns NaN.
        This function may not work correctly if there is infinite number of
        intersection points.


        Parameters
        ----------
        f1,f2 : callable. These are the given functions

        Returns
        -------
        np.float32
            The area between function and the X axis

        """

        def g(x):
            return f1(x) - f2(x)

        def find_root(func, a, b, tol=1e-6, max_iter=10):
            fa = func(a)
            fb = func(b)
            if fa * fb > 0:
                return None
            for _ in range(max_iter):
                if fb - fa == 0:
                    break
                c = b - fb * (b - a) / (fb - fa)
                fc = func(c)
                if abs(fc) < tol:
                    return c
                if fa * fc < 0:
                    b, fb = c, fc
                else:
                    a, fa = c, fc
            return 0.5 * (a + b)

        x_min, x_max = 0.9, 100.1
        step = 0.01

        intersection_points = []
        x = x_min

        while x < x_max - 1e-9:
            val1 = g(x)
            next_x = min(x + step, x_max)
            val2 = g(next_x)

            if val1 * val2 <= 0:
                root = find_root(g, x, next_x)
                if root is not None:
                    if not intersection_points or abs(root - intersection_points[-1]) > 1e-5:
                        intersection_points.append(root)

            x = next_x

        if len(intersection_points) < 2:
            return np.float32(np.nan)

        intersection_points.sort()

        total_area = 0.0
        for i in range(len(intersection_points) - 1):
            a, b = intersection_points[i], intersection_points[i + 1]

            def abs_diff(x):
                return abs(f1(x) - f2(x))

            total_area += float(self.integrate(abs_diff, a, b, n=200))

        return np.float32(total_area)

##########################################################################


import unittest
from sampleFunctions import *
from tqdm import tqdm


class TestAssignment3(unittest.TestCase):

    def test_integrate_float32(self):
        ass3 = Assignment3()
        f1 = np.poly1d([-1, 0, 1])
        r = ass3.integrate(f1, -1, 1, 10)
        self.assertEqual(r.dtype, np.float32)

    def test_integrate_hard_case(self):
        ass3 = Assignment3()
        f1 = strong_oscilations()
        r = ass3.integrate(f1, 0.09, 10, 20)
        print("Result:", r)
        true_result = -7.78662 * 10 ** 33
        print("true result", true_result)
        self.assertGreaterEqual(0.001, abs((r - true_result) / true_result))


if __name__ == "__main__":
    unittest.main()




