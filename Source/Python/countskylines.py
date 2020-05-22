''' Counts the number of size k skylines on an n x n grid '''

import sys
import math

def nCr(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
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

def main():
    if len(sys.argv) < 3:
        print("Usage: countskylines n k")
        return

    n = int(sys.argv[1])
    k = int(sys.argv[2])

    # count[a][b]c] = number of skylines of size c to the right of and below (a, b), given one point must be at (a, b)
    count = [[[0 for i in range(k + 1)] for j in range(n + 1)] for l in range(n + 1)]
    for i in range(1, k + 1):
        for j in range(n + 1):
            for l in range(n + 1):
                if i == 1:
                    count[j][l][i] = 1
                elif (n - j) * (l - 1) >= i - 1:
                    # try all possible next points
                    for x in range(j + 1, n + 1):
                        for y in range(l):
                            count[j][l][i] += count[x][y][i - 1]
    
    print("Skyline count:", count[0][n][k])
    print("Combinations :", nCr((n - 1) ** 2, k))



if __name__ == "__main__":
    main()
