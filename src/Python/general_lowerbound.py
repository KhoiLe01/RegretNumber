import os
import subprocess
import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D
import itertools
import math
import platform

def lowerbound(k, d, sol_count):
    f = open("dD_lowerbound.py", "r+")
    f.truncate(0)
    f.write("import gurobipy as gp\nfrom gurobipy import GRB\n\n")
    f.write("m = gp.Model(\"qp\")\n\n")
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
    f.write("m.setObjective(x, GRB.MAXIMIZE)\n\n\n")

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

    f.write("m.Params.NonConvex = 2\n")
    f.write("m.Params.PoolSearchMode = 2\n")
    f.write("m.Params.PoolSolutions = "+str(sol_count)+"\n\n")

    f.write("m.optimize()\n\n")

    f.write("print(\"All Solutions:\")\n")
    f.write("for i in range (0, m.SolCount):\n")
    f.write("\tprint(\"\\nSolution \"+ str(i+1) + \":\")\n")
    f.write("\tm.Params.SolutionNumber = i\n")
    f.write("\tprint(m.PoolObjVal)\n")
    f.write("\tfor v in m.getVars():\n")
    f.write("\t\tprint('%s %g' % (v.varName, v.xn))\n\n")

    f.write("")

    f.close()

    #return subprocess.check_output("gurobi.sh dD_lowerbound.py", shell=True)

def graph2d(k, d):
    p = lowerbound(k, d)

    p = p.decode()
    p = p.split("\r\n")

    v = []
    points = []
    for i in p:
        if len(i) != 0 and i[0] == "x":
            print("Max x = "+i[2:])
        if len(i) != 0 and i[0] == "p":
            points.append(float(i[4:]))
        if len(i) != 0 and i[0] == "v":
            v.append(float(i[4:]))

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
    for i in range (len(x)):
        x[i] = x[i]/maxx
        y[i] = y[i]/maxy

    print(x)
    print(y)
    print("\t")
    print(vx)
    print(vy)

    pyplot.scatter(x,y)
    pyplot.xlabel("x-coor")
    pyplot.ylabel("y-coor")
    pyplot.show()

def graph3d(k, d):
    p = lowerbound(k, d)

    p = p.decode()
    p = p.split("\r\n")

    v = []
    points = []
    for i in p:
        if len(i) != 0 and i[0] == "x":
            print("Max x = "+i[2:])
        if len(i) != 0 and i[0] == "p":
            points.append(float(i[4:]))
        if len(i) != 0 and i[0] == "v":
            v.append(float(i[4:]))

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

    maxx = max(x)
    maxy = max(y)
    maxz = max(z)
    for i in range (len(x)):
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

def main():
    d = input("What is the value of d?\n")
    while d.isdigit() == False:
        print('Please input a positive integer.\n')
        d = input("What is the value of d?\n")

    k = input("What is the value of k?\n")
    while k.isdigit() == False and k >= d:
        print('Please input a positive integer.\n')
        d = input("What is the value of k?\n")

    sol_count = input("How many solutions should be computed?\n")
    while k.isdigit() == False:
        print('Please input a positive integer.\n')
        d = input("How many solutions should be computed?\n")

    lowerbound(int(k), int(d), int(sol_count))
    if platform.system() == "Windows":
        os.system("gurobi.bat dD_lowerbound.py")
    elif platform.system() == "Linux":
        os.system("gurobi.sh dD_lowerbound.py")

main()
