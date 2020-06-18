#!/usr/bin/env python3

''' 
This program is to help solidify some intuition about the problem
of finding the maximum utility point for a user using as few
queries as possible in which the user must compare points from
the database.

Author : Ashwin Lall
Started: 2017-04-12
''' 

from math import *
import random

PI = 3.1415926535897932384626433

def sphere_point(radius, theta, phi, res):
    ''' Translates polar points to Cartesian using ISO '''
    x = int(radius * cos(2 * PI * phi / res) * sin(PI * theta / res))
    y = int(radius * sin(2 * PI * phi / res) * sin(PI * theta / res))
    z = int(radius * cos(PI * theta / res))
    return (x, y, z)


def main():
    res = 4 # pick a multiple of 4
    radius = 1000
    points = []
    for theta in range(res//2 + 1):
        for phi in range(res//4 + 1):
            point = sphere_point(radius, theta, phi, res)
            if point not in points:
                points.append(point)

    triangles = []
    for theta in range(res//2):
        for phi in range(res//4):
            point1 = sphere_point(radius, theta, phi, res)
            point2 = sphere_point(radius, theta + 1, phi, res)
            point3 = sphere_point(radius, theta + 1, phi + 1, res)
            if point1 != point2 and point1 != point3 and point2 != point3:
                triangles.append((point1, point2, point3))

            point1 = sphere_point(radius, theta, phi, res)
            point2 = sphere_point(radius, theta, phi + 1, res)
            point3 = sphere_point(radius, theta + 1, phi + 1, res)
            if point1 != point2 and point1 != point3 and point2 != point3:
                triangles.append((point1, point2, point3))


    print(len(points), points)
    print(triangles)

if __name__ == "__main__":
    main()
