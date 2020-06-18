import random

def dominates(p1, p2):
    for i in range(len(p1)):
        if p1[i] < p2[i]:
            return False
    return True

def no_dominances(x, y, z):
    d = len(x)
    for i in range(d):
        for j in range(d):
            if i !=j and dominates([x[i], y[i], z[i]], [x[j], y[j], z[j]]):
                return False
    return True

def main():
    max_int = 10
    while True:
        x = [random.randint(1, max_int) for i in range(3)]
        y = [random.randint(1, max_int) for i in range(3)]
        z = [random.randint(1, max_int) for i in range(3)]

        if no_dominances(x, y, z):
            for i in range(3):
                print("p", i + 1, ": (", x[i], y[i], z[i], ")")


            # equation of the plane
            x_coeff = (z[0] - z[1]) * (y[2] - y[0]) + (z[2] - z[0]) * (y[1] - y[0])
            y_coeff = (z[0] - z[1]) * (x[0] - x[2]) + (z[2] - z[0]) * (x[0] - x[1])
            z_coeff = (x[1] - x[0]) * (y[2] - y[0]) + (x[2] - x[0]) * (y[0] - y[1])
            constant = x[0] * x_coeff + y[0] * y_coeff + z[0] * z_coeff
            print("Equation of everything below the plane:")
            if constant >= 0:
                print(x_coeff, "* x +", y_coeff, "* y +", z_coeff, "* z <=", constant)
            else:
                print(-x_coeff, "* x +", -y_coeff, "* y +", -z_coeff, "* z <=", -constant)

            #for i in range(3):
            #    print(x[i] * x_coeff + y[i] * y_coeff + z[i] * z_coeff - constant)

            D = (x[0] - x[1]) * (y[0] - y[2]) - (y[0] - y[1]) * (x[0] - x[2])
            print("D =", D)

            print("R = (", (y[2] - y[0]), "* x +", (x[0] - x[2]), "* y +", x[0] * (y[0] - y[2]) + y[0] * (x[2] - x[0]), ") /", D) 
            print("S = (", (y[0] - y[1]), "* x +", (x[1] - x[0]), "* y +", x[0] * (y[1] - y[0]) + y[0] * (x[0] - x[1]), ") /", D) 

            if D >= 0:
                print("We need:")
                print((y[2] - y[0]), "* x +", (x[0] - x[2]), "* y >=", x[0] * (y[2] - y[0]) + y[0] * (x[0] - x[2])) 
                print((y[0] - y[1]), "* x +", (x[1] - x[0]), "* y >=", x[0] * (y[0] - y[1]) + y[0] * (x[1] - x[0])) 
            else:
                print("We need:")
                print((y[2] - y[0]), "* x +", (x[0] - x[2]), "* y <=", x[0] * (y[2] - y[0]) + y[0] * (x[0] - x[2])) 
                print((y[0] - y[1]), "* x +", (x[1] - x[0]), "* y <=", x[0] * (y[0] - y[1]) + y[0] * (x[1] - x[0]))
            input("Press enter for next example.\n\n")


main()
