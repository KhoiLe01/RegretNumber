import math

def lower_upper(k, d):
    ''' prints the known upper and lower bounds for rho(k, d) '''
    lower = 1 / (8 * math.pow(2 * k, (d - 1)/2.0))
    upper_cube = (d - 1.0) / (int(math.pow(k - d + 1, 1.0/(d - 1))) + d - 1)
  
    if d <= k < 2 * d:
        upper_sphere = 1 - 1 / (d * math.sqrt(d))
    elif 2 * d <= k < d * d + d:
        upper_sphere = d * (d - 1) / (.25 + d * (d - 1))
    else:
        upper_sphere = d * (d - 1) / (pow((k - d)/(d * d), 2.0/(d - 1)) + d * (d - 1))

    print("%0.4f <= rho(%d, %d) <= min(%0.4f, %0.4f)" % (lower, k, d, upper_cube, upper_sphere))


def main():
    for d in range(2, 7):
        for k in range(d, 7):
            lower_upper(k, d)

if __name__ == "__main__":
    main()
