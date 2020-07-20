"""
general_lowerbound.py
Khoi Le, Derek Sun, Ashwin Lall
"""

import os
import sys
import subprocess
import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D
import itertools
import math
import platform

"""
Generates Python file for Gurobi model
Inputs:
k - size of output subset
d - number of attributes
sol_count - number of optimal solutions for Gurobi to output
"""
def lowerbound(k, d, sol_count):
    #  open or create Gurobi model file if it doesn't exist
    f = open("dD_lowerbound.py", "r+")
    f.truncate(0)

    f.write("import gurobipy as gp\nfrom gurobipy import GRB\n\n")
    f.write("m = gp.Model(\"qp\")\n\n")
    # initiate Gurobi model variables
    f.write("x = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"x\")\n\n")
    for i in range (1,k+2):
        for j in range (1,d+1):
            f.write("v"+str(i)+str(j)+" = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"v"+str(i)+str(j)+"\")\n")
        f.write("\n")
    f.write("\n")
    for i in range (1,k+2):
        for j in range (1,d+1):
            f.write("p"+str(i)+str(j)+" = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"p"+str(i)+str(j)+"\")\n")
        f.write("\n")
    f.write("\n\n")
    # maximize x variable
    f.write("m.setObjective(x, GRB.MAXIMIZE)\n\n\n")

    # initiate Gurobi model constraints
    for i in range (1, k+1):
        f.write("m.addConstr(p"+str(i)+"1<=p"+str(i+1)+"1, \"c0"+str(i)+"\")\n")

    f.write("\n\n")

    for i in range (1,k+2):
        f.write("m.addConstr(p"+str(i)+str(1)+"*v"+str(i)+str(1))
        for j in range (2,d+1):
            f.write("+p"+str(i)+str(j)+"*v"+str(i)+str(j))
        f.write("==1, \"c"+str(i)+str(1)+"\")\n")

        for h in range (1,k+2):
            if h!=i:
                f.write("m.addConstr(1")
                for q in range (1,d+1):
                    f.write("-p" + str(h) + str(q) + "*v" + str(i) + str(q))
                f.write(">=x, \"c"+str(i)+str(h+1)+"\")\n")
        f.write("\n")

    f.write("\n")

    # set Gurobi model to NonConvex mode
    f.write("m.Params.NonConvex = 2\n")
    # allow multiple optimal solutions
    f.write("m.Params.PoolSearchMode = 2\n")
    f.write("m.Params.PoolSolutions = "+str(sol_count)+"\n\n")

    f.write("m.optimize()\n\n")

    # print out solutions
    f.write("print(\"All Solutions:\")\n")
    f.write("for i in range (0, m.SolCount):\n")
    f.write("\tprint(\"\\nSolution \"+ str(i+1))\n")
    f.write("\tm.Params.SolutionNumber = i\n")
    f.write("\tprint(m.PoolObjVal)\n")
    f.write("\tfor v in m.getVars():\n")
    f.write("\t\tprint('%s %g' % (v.varName, v.xn))\n\n")

    f.write("")

    f.close()

"""
Graph results from Gurobi optimization for a 2d database
"""
def graph2d():
    # open text file log
    terminal_log = open("terminal_log.txt", "r+", encoding="utf-8")

    # initialize list and counter variable
    v = []
    points = []
    count = 2

    # parse for data
    for line in terminal_log:
        if len(line) != 0 and line[0] == "x":
            print("Max x = "+line[2:])
        if len(line) != 0 and line[0] == "p":
            points.append(float(line[4:]))
        if len(line) != 0 and line[0] == "v":
            v.append(float(line[4:]))
        # plot graph for each solution
        if line[:8] == "Solution" and line[9:].strip() == str(count):
            x = []
            y = []

            vx = []
            vy = []

            # sort data by category
            for i in range(len(points)):
                if i % 2 == 0:
                    x.append(points[i])
                    vx.append(v[i])
                else:
                    y.append(points[i])
                    vy.append(points[i])

            # rescale points
            maxx = max(x)
            maxy = max(y)

            for i in range(len(x)):
                x[i] = x[i] / maxx
                y[i] = y[i] / maxy

            # print data
            print(x)
            print(y)
            print("\t")
            print(vx)
            print(vy)

            # plot data
            pyplot.scatter(x, y)
            pyplot.xlabel("x-coor")
            pyplot.ylabel("y-coor")
            pyplot.show()

            # reset lists and increment counter
            count += 1
            v = []
            points = []

    # plot graph for last solution
    x = []
    y = []

    vx = []
    vy = []

    for i in range(len(points)):
        if i % 2 == 0:
            x.append(points[i])
            vx.append(v[i])
        else:
            y.append(points[i])
            vy.append(points[i])

    maxx = max(x)
    maxy = max(y)

    for i in range(len(x)):
        x[i] = x[i] / maxx
        y[i] = y[i] / maxy

    print(x)
    print(y)
    print("\t")
    print(vx)
    print(vy)

    pyplot.scatter(x, y)
    pyplot.xlabel("x-coor")
    pyplot.ylabel("y-coor")
    pyplot.show()


"""
Graph results from Gurobi optimization for a 3d database
"""
def graph3d():
    # open text file log
    terminal_log = open("terminal_log.txt", "r+", encoding="utf-8")

    # initialize list and counter variable
    v = []
    points = []
    count = 2

    # parse for data
    for line in terminal_log:
        if len(line) != 0 and line[0] == "x":
            print("Max x = "+line[2:])
        if len(line) != 0 and line[0] == "p":
            points.append(float(line[4:]))
        if len(line) != 0 and line[0] == "v":
            v.append(float(line[4:]))
        # plot graph for each solution
        if line[:8] == "Solution" and line[9:].strip() == str(count):
            x = []
            y = []
            z = []

            vx = []
            vy = []
            vz = []

            # sort data by category
            for i in range(len(points)):
                if i % 3 == 0:
                    x.append(points[i])
                    vx.append(v[i])
                elif i % 3 == 1:
                    y.append(points[i])
                    vy.append(points[i])
                else:
                    z.append(points[i])
                    vz.append(points[i])

            for i in range(len(x)):
                print(x[i]*vx[i]+y[i]*vy[i]+z[i]*vz[i])

            # rescale points
            maxx = max(x)
            maxy = max(y)
            maxz = max(z)
            for i in range (len(x)):
                x[i] = x[i]/maxx
                y[i] = y[i]/maxy
                z[i] = z[i]/maxz

            # print data
            print(x)
            print(y)
            print(z)
            print("\t")
            print(vx)
            print(vy)
            print(vz)

            # plot data
            fig = pyplot.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(x, y, z, c='r', marker='o')
            ax.set_xlabel('X Label')
            ax.set_ylabel('Y Label')
            ax.set_zlabel('Z Label')
            pyplot.show()

            # reset lists and increment counter
            count += 1
            v = []
            points = []

    # plot graph for last solution
    x = []
    y = []
    z = []

    vx = []
    vy = []
    vz = []

    for i in range(len(points)):
        if i % 3 == 0:
            x.append(points[i])
            vx.append(v[i])
        elif i % 3 == 1:
            y.append(points[i])
            vy.append(points[i])
        else:
            z.append(points[i])
            vz.append(points[i])

    for i in range(len(x)):
        print(x[i]*vx[i]+y[i]*vy[i]+z[i]*vz[i])

    maxx = max(x)
    maxy = max(y)
    maxz = max(z)
    for i in range(len(x)):
        x[i] = x[i]/maxx
        y[i] = y[i]/maxy
        z[i] = z[i]/maxz

    print(x)
    print(y)
    print(z)
    print("\t")
    print(vx)
    print(vy)
    print(vz)

    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x, y, z, c='r', marker='o')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    pyplot.show()

"""
Verify if data obtained from Gurobi supports our conjecture
Inputs:
k - size of output subset
d - number of attributes
sol_count - number of optimal solutions for Gurobi to output
"""
def verify(d, k, sol_count):
    # open text file log
    terminal_log = open("terminal_log.txt", "r+", encoding="utf-8")

    v = []
    points = []

    # parse data from terminal_log
    for line in terminal_log:
        if len(line) != 0 and line[0] == "x":
            print("Max x = "+line[2:])
        if len(line) != 0 and line[0] == "p":
            points.append(float(line[4:]))
        if len(line) != 0 and line[0] == "v":
            v.append(float(line[4:]))

    # verify data
    for h in range(0, sol_count):
        for j in range(0,d):
            count = -d-j
            for i in range(0,k+1):
                count += d
                if v[count+h*(k+1)*d] == 0:
                    print("0/0")
                    continue
                print(points[count+h*(k+1)*d]/v[count+h*(k+1)*d])
            print("\n")

"""
main function
"""
def main():
    # prompt user for value of d variable
    d = input("What is the value of d?\n")
    # while value is invalid, prompt user again
    while d.isdigit() == False:
        print('Please input a positive integer.\n')
        d = input("What is the value of d?\n")

    # prompt user for value of k variable
    k = input("What is the value of k?\n")
    while k.isdigit() == False or int(k) < int(d):
        print('Please input a positive integer that is >= d.\n')
        k = input("What is the value of k?\n")

    # prompt user for value of sol_count variable
    sol_count = input("How many solutions should be computed?\n")
    while sol_count.isdigit() == False:
        print('Please input a positive integer.\n')
        sol_count = input("How many solutions should be computed?\n")

    # prompt user to see if data needs to be graphed
    graph_input = input("Should the solutions be graphed?\n").upper()
    while graph_input not in {'YES', 'NO', 'Y', 'N'}:
        print('Please input yes or no.\n')
        graph_input = input("Should the solutions be graphed?\n").upper()

    # if data needs to be graphed
    if graph_input in ['YES', 'Y']:
        # 2d case
        if int(d) == 2:
            # generate Gurobi model and terminal_log.txt file
            lowerbound(int(k), int(d), int(sol_count))
            # if user is using Windows use gurobi.bat
            if platform.system() == "Windows":
                os.system("gurobi.bat dD_lowerbound.py > terminal_log.txt")
            # if user is using Linux use gurobi.sh
            elif platform.system() == "Linux":
                os.system("gurobi.sh dD_lowerbound.py")
            graph2d()
            return
        # 3d case
        elif int(d) == 3:
            lowerbound(int(k), int(d), int(sol_count))
            if platform.system() == "Windows":
                os.system("gurobi.bat dD_lowerbound.py > terminal_log.txt")
            elif platform.system() == "Linux":
                os.system("gurobi.sh dD_lowerbound.py")
            graph3d()
            return
        # only 2d and 3d case can be graphed
        print('(graphing is only supported for 2d + 3d cases)')
        return

    # if data does not need to be graphed
    lowerbound(int(k), int(d), int(sol_count))
    if platform.system() == "Windows":
        os.system("gurobi.bat dD_lowerbound.py > terminal_log.txt")
        verify(int(d), int(k), int(sol_count))
    elif platform.system() == "Linux":
        os.system("gurobi.sh dD_lowerbound.py")

main()
