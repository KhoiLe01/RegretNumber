#!/usr/bin/env python3

'''
This program aims to find counterexamples for conjectures made about
how regret minimization works

Author : Ashwin Lall
Started: 2017-02-11
'''

import math
import random
import time
import itertools
import sys
from regretnumbers import *

def check_counterexample(d, k, n, points, utility_repeats=1000):
    ''' check if this set of points violates our conjecture '''
    worst_regret = smallest_set_regret(points, k, utility_repeats)

    # now pick a point and move it to the hypersphere
    index = random.randint(0, n - 1)
    largest_worst_regret = 0
    for dim in range(d):
        # move point[index] in the dim-th dimension
        temp =  points[index][dim]
        points[index][dim] = math.sqrt(1 - sum([x**2 for x in points[index]]) + points[index][dim]**2)
        regret = smallest_set_regret(points, k, utility_repeats)
        if regret > largest_worst_regret:
            largest_worst_regret = regret
        points[index][dim] = temp

    if worst_regret > largest_worst_regret:
        print("Counter example!")
        print(d, k, n)
        print(points, worst_regret)
        print(points[index], largest_worst_regret)

    return worst_regret > largest_worst_regret

def check_counterexample_full_set(d, k, n, points, utility_repeats=1000):
    ''' check if this set of points violates our conjecture '''
    points_scaled = []
    for point in points:
        norm = math.sqrt(sum([i**2 for i in point]))
        points_scaled.append([point[i]/norm for i in range(d)])
    
    worst_regret = smallest_set_regret(points, k, utility_repeats)
    worst_regret_scaled = smallest_set_regret(points_scaled, k, utility_repeats)

    if worst_regret > worst_regret_scaled:
        print("Counter example!")
        print(d, k, n)
        print(points, worst_regret)
        print(points_scaled, worst_regret_scaled)
        return True
    return False

def check_counterexample_each_set(d, k, n, points, utility_repeats=1000):
    ''' check if this set of points violates our conjecture '''
    points_scaled = []
    for point in points:
        norm = math.sqrt(sum([i**2 for i in point]))
        points_scaled.append([point[i]/norm for i in range(d)])
    
    for indexes in itertools.combinations(range(d), k): # for each subset of exactly k indexes
        subset = [points[i] for i in indexes]
        subset_scaled = [points_scaled[i] for i in indexes]
        
        # compute worst case regret for this set
        worst_regret = set_regret(points, subset, utility_repeats)
        worst_regret_scaled = set_regret(points_scaled, subset_scaled, utility_repeats)

        if worst_regret > worst_regret_scaled:
            print("Counter example!")
            print(d, k, n)
            print(points)
            print(points_scaled)
            print(subset, worst_regret)
            print(subset_scaled, worst_regret_scaled)
            return True
    return False


def main():
    while True:
        d = random.randint(2, 2)
        k = random.randint(d, d + 0)
        n = random.randint(k + 1, k + 1)
        points = [[random.random() for i in range(d)] for j in range(n)]
        #points = [[random.randint(1, 5)/5.0 for i in range(d)] for j in range(n)]

        # normalize points to make largest distance equal to 1
        max_dist = 0
        for i in range(n):
            max_dist = max(max_dist, math.sqrt(dot(points[i], points[i])))
        points = [[points[j][i]/max_dist for i in range(d)] for j in range(n)]

        if not has_dominances(points):
            if check_counterexample(d, k, n, points):
                return

if __name__ == "__main__":
    main()
