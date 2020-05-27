''' 
Program to search for the best way to fit k points on the positive part of a d-sphere 
such that the angle between any two points is as large as possible
'''

import random
import math
import sys
import time

def dot(x, y):
    ''' computes dot product of two vectors (assume x and y have same length) '''
    return sum([x[i] * y[i] for i in range(len(x))])

def normalize(point):
    ''' re-scale this point so that it is on the unit d-sphere '''
    magnitude = math.sqrt(sum([point[j] ** 2 for j in range(len(point))]))
    for j in range(len(point)):
        point[j] /= magnitude

def closest(points):
    ''' computes the pair of points with the smallest angle between them '''
    largest_cosine = 0.0
    point_1, point_2 = 0, 0
    k, d = len(points), len(points[0])
    for i in range(k):
        for j in range(i + 1, k):
            cosine = dot(points[i], points[j])
            if cosine > largest_cosine:
                largest_cosine = cosine
                point_1, point_2 = i, j
    return point_1, point_2

def compute_rho(k, d):
    ''' Estimates rho(k, d), assuming that the worst case involves k+1 points on the d-sphere '''
    points = [[random.random() for i in range(d)] for j in range(k + 1)]
    # re-normalize onto d-sphere
    for i in range(k + 1):
        normalize(points[i])

    # relaxation factor
    epsilon = 0.001

    # change threshold for stopping
    delta = 1e-5

    iter = 0
    cosine, old_cosine = 1.0, 0.0
    while math.fabs(cosine - old_cosine) > delta and iter < 1000000:
        # find the (index of the) closest pair of points
        i_1, i_2 = closest(points)

        iter += 1
        if iter % 100000 == 0:
            old_cosine = cosine
            cosine = dot(points[i_1], points[i_2])
            print(iter)
            print(dot(points[i_1], points[i_2]))
            print(points)
            print()

        # move these two points slightly apart
        new_1 = [min(1, max(0, points[i_1][j] + epsilon * (points[i_1][j] - points[i_2][j]))) for j in range(d)]
        new_2 = [min(1, max(0, points[i_2][j] + epsilon * (points[i_2][j] - points[i_1][j]))) for j in range(d)]
        points[i_1] = new_1
        normalize(points[i_1])
        points[i_2] = new_2
        normalize(points[i_2])

    #print(cosine)
    #print(points)
    return points, cosine

def compute_rho_table():
    ''' computes a table of rho values '''
    MAX_D = 7
    MAX_K = 20
    table = [[1.0 for i in range(MAX_D + 1)] for j in range(MAX_K + 1)]
    for d in range(2, MAX_D + 1):
        for k in range(d, MAX_K + 1):
            print(k,d)
            points, cosine = compute_rho(k, d)
            table[k][d] = 1.0 - cosine

    print(table)

    # write to file
    current_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime())
    file = open("rho_table_" + current_time + ".csv", "w")
    file.write("," + ",".join([str(d) for d in range(2, MAX_D + 1)]) + "\n")
    for k in range(2, MAX_K + 1):
        file.write(str(k) + "," + ",".join(str(table[k][d]) for d in range(2, MAX_D + 1)) + "\n")
    file.close()
            
   

def main():
    if len(sys.argv) == 1:
        compute_rho_table()
    elif len(sys.argv) == 3:
         k = int(sys.argv[1])
         d = int(sys.argv[2])
         print(compute_rho(k, d))
    else:
        print("Usage: relax k d")
        sys.exit()

if __name__ == "__main__":
    main()
