#!/usr/bin/env python3

''' 
This program aims to compute bounds for varios regret numbers.
Regret numbers are defined as follows:
Let rho(k, d) be the smallest regret ratio possible when selecting exactly k tuples 
from a database of d-dimensional tuples, assuming linear utility functions.

Author : Ashwin Lall
Started: 2017-01-17
''' 

import math
import random
import time
import itertools
import sys

def lower_upper(k, d):
    ''' prints the known upper and lower bounds for rho(k, d) '''
    lower = 1 / (8 * math.pow(2 * k, (d - 1)/2.0))
    upper = (d - 1.0) / (int(math.pow(k - d + 1, 1.0/(d - 1))) + d - 1)
    print("%0.4f <= rho(%d, %d) <= %0.4f" % (lower, k, d, upper))

def dot(v1, v2):
    ''' computes the dot product of two vectors 
        (assumes that vectors are of equal length)
    '''
    return sum([v1[i] * v2[i] for i in range(len(v1))]) 


def regret(p, points, utility_repeats=1000):
    ''' returns the maximum regret for omitting p and including points 
        found using 'utility_repeats' random utility functions 
    '''
    d = len(p)
    worst = 0.0  # worst regret ratio for omitting the point p
    for j in range(utility_repeats):
        # generate a random utility function
        utility = [random.random() for i in range(d)]
        
        # find the lowest regret among the other points
        best = 1.0
        for l in range(len(points)):
            regret = 1.0 - dot(points[l], utility)/dot(p, utility)
            best = min(best, regret)

        # update the worst case regret we've seen so far
        worst = max(worst, best)

    return worst
        
def set_regret(all_points, subset, utility_repeats=1000):
    ''' returns the maximum regret for including only the given subset
        instead of all_points using 'utility_repeats' random utility functions
    '''
    # compute worst case regret for this set                                                                          
    worst_regret = 0.0
    for point in all_points:
        if point not in subset:
            point_regret = regret(point, subset, utility_repeats)
            worst_regret = max(worst_regret, point_regret)
    return worst_regret

def smallest_set_regret(all_points, k, utility_repeats=1000):
    ''' returns the smallest regret when selecting precisely k of all_points '''
    smallest_regret = 1.0 # smallest regret for showing k points
    for set in itertools.combinations(all_points, k): # for each subset of exactly k points
        # compute worst case regret for this set
        worst_regret = set_regret(all_points, set, utility_repeats)
        smallest_regret = min(smallest_regret, worst_regret)
    return smallest_regret

def rescaled(points):
    ''' rescales a set of points so that the maximum is 1 in each dimension '''
    n = len(points)
    d = len(points[0])
    rescaledpoints = [[0 for i in range(d)] for j in range(n)]
    for i in range(d):
        max = points[0][i]
        for j in range(1, n):
            if points[j][i] > max:
                max = points[j][i]
        for j in range(n):
            rescaledpoints[j][i] = points[j][i]/max
    return rescaledpoints


"""
def lower_bound_random_search_omitting_one(k, d, repeats = 1000, utility_repeats = 100):
    ''' randomly generates a database of k+1 random points
        and computes the worst regret ratio for omitting one.
        return the largest such regret ratio after repeats utility_repeats
    '''
    min_regret = 0.0  # the largest minimum regret we've found so far
    worst_points = [[0 for i in range(d)] for j in range(k+1)] # initialize to something
    for r in range(repeats):
        # generate k+1 random d-dimensional points
        points = [[random.random() for i in range(d)] for j in range(k+1)]

        smallest_regret = 1.0 # smallest regret for omitting a single point
        for i in range(k + 1):  # compute the regret for omitting the i-th point
            point_regret = regret(points[i], points[:i] + points[i+1:], utility_repeats)
            smallest_regret = min(smallest_regret, point_regret)

        if min_regret < smallest_regret:
            min_regret = smallest_regret
            worst_points = points

    return min_regret, worst_points
"""

def lower_bound_random_search(k, d, n, repeats = 1000, utility_repeats = 100):
    ''' randomly generates a database of n random points
        and computes the lowest maximum regret ratio for a set of k points 
        return the largest such regret ratio after repeats utility_repeats
    '''
    largest_min_regret = 0.0  # the largest minimum regret we've found so far
    worst_points = [[0 for i in range(d)] for j in range(k+1)] # initialize to something
    for r in range(repeats):
        # generate n random d-dimensional points

        points = [[random.random() for i in range(d)] for j in range(n)]
        while has_dominances(points):
            points = [[random.random() for i in range(d)] for j in range(n)]
        
        # compute smallest regret from a subset of exactly k of these points
        smallest_regret = smallest_set_regret(points, k, utility_repeats)

        if largest_min_regret < smallest_regret:
            largest_min_regret = smallest_regret
            worst_points = points

    return largest_min_regret, worst_points
        
    
def group_search(k_values, d_values, repeats = 1000, utility_repeats = 100):
    ''' performs a random search for each of the combination of k and d values in
        the given arrays and keeps an updated lower bound for each 
    '''
    bound = {}
    count = {}
    for k in k_values:
        for d in d_values:
            bound[(k, d)] = 0.0
            count[(k, d)] = 0    # count the number of trials so far

    start_time = time.clock()
    iterations = 0
    while True:
        # randomly generate a k and d value such that k >= d
        k = 0
        d = 1
        while k < d:
            k = random.choice(k_values)
            d = random.choice(d_values)
        count[(k, d)] += 1
        iterations += 1
            
        # compute the pair of k/d that has the smallest number of tries 
        min_count = count[(k, d)]
        for (k1, d1) in count:
            if k1 >= d1:
                min_count = min(count[(k1, d1)], min_count)

        # perform regret computation and update if better than current
        min_regret, worst_points = lower_bound_random_search(k, d, k + 1, repeats, utility_repeats)
        if min_regret > bound[(k, d)]:
            bound[(k, d)] = min_regret
        
        # print to screen every minute
        if time.clock() - start_time >= 5.0:
             print(iterations, min_count)

             for d in d_values:
                print("\t", d, end="")
             print()
             for k in k_values:
                 print(k, end="")
                 for d in d_values:
                     if k >= d:
                         print("\t%0.4f" % bound[(k, d)], end="")
                     else:
                         print("\t-", end="")
                 print()
             print()
             start_time = time.clock()


def group_search_compare(k_values, d_values, repeats = 1000, utility_repeats = 100):
    ''' performs a random search for each of the combination of k and d values in
        the given arrays and keeps an updated lower bound for each
        This one is different from the one above in that it compares the answer for
        trying n=k+1 and n=k+2
    '''
    bound2 = {}
    bound1 = {}
    count = {}
    worstpts1 = {}
    worstpts2 = {}
    for k in k_values:
        for d in d_values:
            bound2[(k, d)] = 0.0
            bound1[(k, d)] = 0.0
            count[(k, d)] = 0    # count the number of trials so far
            worstpts1[(k, d)] = []
            worstpts2[(k, d)] = []

    start_time = time.clock()
    iterations = 0
    while True:
        # randomly generate a k and d value such that k >= d
        k = 0
        d = 1
        while k < d:
            k = random.choice(k_values)
            d = random.choice(d_values)
        count[(k, d)] += 1
        iterations += 1

        # compute the pair of k/d that has the smallest number of tries
        min_count = count[(k, d)]
        for (k1, d1) in count:
            if k1 >= d1:
                min_count = min(count[(k1, d1)], min_count)

        # perform regret computation and update if better than current with n = k + 1
        min_regret, worst_points = lower_bound_random_search(k, d, k + 1, repeats, utility_repeats)
        if min_regret > bound1[(k, d)]:
            bound1[(k, d)] = min_regret
            worstpts1[(k, d)] = sorted(rescaled(worst_points), key=lambda point:point[0])  # scale so that max in each dim is 1 and sort by first dim

        # perform regret computation and update if better than current with n = k + 2
        min_regret, worst_points = lower_bound_random_search(k, d, k + 2, repeats, utility_repeats)
        if min_regret > bound2[(k, d)]:
            bound2[(k, d)] = min_regret
            worstpts2[(k, d)] = sorted(rescaled(worst_points), key=lambda point:point[0])  # scale so that max in each dim is 1 and sort by first dim 

        # print to screen every 5 seconds
        if time.clock() - start_time >= 5.0:
             print(iterations, min_count)

             print("With n = k + 1")
             for d in d_values:
                print("\t", d, end="")
             print()
             for k in k_values:
                 print(k, end="")
                 for d in d_values:
                     if k >= d:
                         print("\t%0.4f" % bound1[(k, d)], worstpts1[(k, d)], end="")
                     else:
                         print("\t-", end="")
                 print()
             print()

             print("With n = k + 2")
             for d in d_values:
                print("\t", d, end="")
             print()
             for k in k_values:
                 print(k, end="")
                 for d in d_values:
                     if k >= d:
                         print("\t%0.4f" % bound2[(k, d)], worstpts2[(k, d)], end="")
                     else:
                         print("\t-", end="")
                 print()
             print()

             start_time = time.clock()


def dominates(x, y):
    ''' checks of x dominates y -- that is, x is at least as big in every dimension and strictly bigger in at least one '''
    strict = False
    for i in range(len(x)):
        if x[i] < y[i]:
            return False
        elif x[i] > y[i]:
            strict = True
    return strict

def has_dominances(set):
    ''' checks if any points dominate each other in this set '''
    for x in set:
        for y in set:
            if x != y and dominates(x, y):
                return True
    return False


def choose(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
    http://stackoverflow.com/questions/3025162/statistics-combinations-in-python/3025194#3025194
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

def one_in_each_dim(set):
    ''' Checks to make sure that the largest value in each dimension is 1 '''
    d = len(set[0])
    largest = [0 for i in range(d)]
    for point in set:
        for i in range(d):
            largest[i] = max(largest[i], point[i])
    
    for i in range(d):
        if largest[i] < 1.0:
            return False
    return True


def grid_search(k, d, n, c, utility_repeats):
    ''' Does a discretized space search in which each dimension is divided into c equal chunks
        and from all possible cubes all combinations of n are picked so that the best subset of
        k of these n has the largest possible regret
    '''
    # generate cubes of width 1/c in each dimension
    chunks = [i * 1.0/c for i in range(1, c + 1)]
    all_cubes = itertools.product(chunks, repeat=d)
    
    largest_min_regret = 0.0
    worst_points = []
    counter = 0
    combinations = choose(c ** d, n)
    for full_set in itertools.combinations(all_cubes, n):
        counter += 1
        if counter % 1000000 == 0:
            print("About", 100.0 * counter / combinations, "percent done.")

        if not has_dominances(full_set): # make sure that no point dominates any other
            if one_in_each_dim(full_set):
                smallest_regret = smallest_set_regret(full_set, k, utility_repeats)

                # record if this full_set had a high minregret
                if smallest_regret > largest_min_regret:
                    largest_min_regret = smallest_regret
                    worst_points = full_set
                    print(largest_min_regret, worst_points)

    return largest_min_regret, worst_points


def refine(k, d, n, width, depth, points, utility_repeats=1000):
    ''' refines the solution 'depth' times assuming that the optimal is within a box of dimensions 'width' around the set of points '''
    largest = 0.0
    best_points = points
    for vector in itertools.product([-1, 1], repeat=d * n): # try all 2^{dn} 2x2...x2 sub-grids
        p = [[points[i][j] + vector[i * d + j] * width / 4.0 for j in range(d)] for i in range(n)] # create new set of points with offset determined by vector
        min_regret = smallest_set_regret(p, k, utility_repeats)
        if min_regret > largest:
            largest = min_regret
            best_points = p
    
    print("depth = ", depth, ":", largest, best_points)
    if depth == 1:
        return largest, best_points
    else:
        return refine(k, d, n, width/2.0, depth - 1, best_points, utility_repeats)


def main():
    #for k in range(2, 10):
    #    lower_upper(k, 2)

    #print(lower_bound_random_search(2, 2, 100000, 10000))
    group_search_compare(range(2, 7), range(2, 3), 1, 100)
    #print(grid_search(2, 2, 3, 20, 100))

##    if len(sys.argv) < 6:
##        print("Usage: python3 regretnumbers k d n c repeats")
##    else:
##        k, d, n, c, repeats = [int(i) for i in sys.argv[1:]]
##        best_regret, points = grid_search(k, d, n, c, repeats)
##     
##        print(best_regret, points)
##        print(refine(k, d, n, 2.0/c, 20, points, 1000))
        

if __name__ == "__main__":
    main()
