"""
In this assignment you should fit a model function of your choice to data
that you sample from a contour of given shape. Then you should calculate
the area of that shape.

The sampled data is very noisy so you should minimize the mean least squares
between the model you fit and the data points you sample.

During the testing of this assignment running time will be constrained. You
receive the maximal running time as an argument for the fitting method. You
must make sure that the fitting function returns at most 5 seconds after the
allowed running time elapses. If you know that your iterations may take more
than 1-2 seconds break out of any optimization loops you have ahead of time.

Note: You are allowed to use any numeric optimization libraries and tools you want
for solving this assignment.
Note: !!!Despite previous note, using reflection to check for the parameters
of the sampled function is considered cheating!!! You are only allowed to
get (x,y) points from the given shape by calling sample().
"""
import math
import numpy as np
import time
import random
from functionUtils import AbstractShape

class MyShape(AbstractShape):
    Random_points_on_shape = []
    orderPoints=[]

    xc = float(0)
    yc = float(0)


    def __init__(self,  Random_points_on_shape ):

        self.Random_points_on_shape = Random_points_on_shape

        self.contour()



    def contour(self):
        minX = float(1000)
        maxX = float(-1000)
        minY = float(1000)
        maxY = float(-1000)
        self.orderPoints.clear()
        self.Cal_ShapCenter()
        PointXYs_Angle = []
        for point in self.Random_points_on_shape:
            ang = self.Cal_angle((self.xc, self.yc), point)
            PointXYs_Angle.append([ang, point])
        PointXYs_Angle.sort(key=lambda Angel: Angel[0])

        self.orderPoints=self.moving_average_circular(PointXYs_Angle,20)

        return self.orderPoints

    def moving_average_circular(self, points, window_size=10):
        half_window = window_size // 2
        n = len(points)
        averaged_points = []
        for i in range(n):
                window_points = []
                for j in range(-half_window, half_window + 1):
                    index = (i + j) % n
                    window_points.append(points[index])
                if window_points:
                    averaged_x = sum(item[1][0] for item in window_points) / len(window_points)
                    averaged_y = sum(item[1][1] for item in window_points) / len(window_points)
                averaged_points.append((averaged_x, averaged_y))
        return averaged_points



    def Cal_ShapCenter(self):
        # חישוב מרכז הכובד של הצורה
        minX=float(1000)
        maxX=float(-1000)
        minY=float(1000)
        maxY=float(-1000)
        for point in self.Random_points_on_shape:
            self.xc += point[0]
            self.yc += point[1]
        self.xc = self.xc / len(self.Random_points_on_shape)
        self.yc = self.yc / len(self.Random_points_on_shape)


    def area(self)->np.float32:

        Center=(self.xc,self.yc)

        area1=float(0)
        for i in range(len(self.orderPoints)-1):

                p1=self.orderPoints[i]
                p2=self.orderPoints[i+1]
                d= self.triangle_area_2d(Center, p1, p2)
                if (d>0.3):
                    d=0.1
                area1=area1+d

        return area1

    def polygonArea(self):
        pts = np.array(self.Random_points_on_shape)
        if pts.shape[0] < 3:
            return 0.0
        x = pts[:, 0]
        y = pts[:, 1]
        area = 0.5 * np.abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
        return area



    def triangle_area_2d(self, p1, p2, p3):
                x1, y1 = p1
                x2, y2 = p2
                x3, y3 = p3
                a=math.sqrt((x1 - x2)**2 + (y1 - y2)**2 )
                b=math.sqrt((x2 - x3)**2 + (y2 - y3)**2)
                c=math.sqrt((x3-x1)**2 + (y3-y1)**2)
                s=(a+b+c)/2
                area=math.sqrt(s*(s-a)*(s-b)*(s-c))
                return area

    def Cal_angle(self,center, point):
        x, y = point
        cx, cy = center

        angle = math.atan2(y - cy, x - cx)
        if angle < 0:
            angle += 2 * math.pi

        return angle*57.297






class Assignment5:
    Random_points_on_shape = []


    xc = float(0)
    yc = float(0)

    def fit_shape(self, sample: callable, maxtime: float) -> AbstractShape:

        self.Random_points_on_shape=[]
        start_time = float (time.time())
        while time.time() - start_time < (maxtime *0.5)  and  len(self.Random_points_on_shape)<10000:
            try:
                x_, y_ = sample()
                self.Random_points_on_shape.append((x_, y_))
            except:
                break

        Shape=MyShape(self.Random_points_on_shape)



        return Shape

    def area(self, contour: callable, maxerr=0.001) -> np.float32:

        sample = 15
        old_area = 0.0

        max_iterations = 10

        for _ in range(max_iterations):
            shape = MyShape(contour(sample))
            new_area = shape.polygonArea()

            if new_area != 0:
                rel_diff = abs(new_area - old_area)
            else:
                rel_diff = abs(new_area - old_area)
            if rel_diff <= maxerr:
                return np.float32(new_area)

            sample = sample*2
            old_area = new_area

        return np.float32(new_area)


##########################################################################


import unittest
from sampleFunctions import *
from tqdm import tqdm


class TestAssignment5(unittest.TestCase):

    def test_return(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=circ, maxtime=2)
        T = time.time() - T
        self.assertTrue(isinstance(shape, AbstractShape))
        self.assertLessEqual(T, 5)

    def test_delay(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)

        def sample():
            time.sleep(7)
            return circ()

        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=sample, maxtime=5)
        T = time.time() - T
       # a = shape.area()
        self.assertTrue(isinstance(shape, AbstractShape))
        self.assertGreaterEqual(T, 5)

    def test_circle_area(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=circ, maxtime=2)
        T = time.time() - T
        a = shape.area()
        self.assertLess(abs(a - np.pi), 0.01)
        self.assertLessEqual(T, 32)

    def test_bezier_fit(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=circ, maxtime=30)
        T = time.time() - T
        a = shape.area()
        self.assertLess(abs(a - np.pi), 0.01)
        self.assertLessEqual(T, 32)


if __name__ == "__main__":
    unittest.main()
