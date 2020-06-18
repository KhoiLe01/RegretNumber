import itertools
import operator as op
from functools import reduce
import subprocess
import os
import platform

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom

def increment(l, n):
    k = len(l)-1
    while l[k] == n-1:
        l[k] = 0
        k -= 1
    l[k] += 1

def all_pos(k, n):
    l1 = [i for i in range (1, k+n+1)]

    l2 = list(itertools.combinations(l1, n))

    l3 = [0 for i in range(len(l2))]

    result = []

    for j in range(2 ** (ncr(k+n, n))):
        partial = []
        for i in range(len(l2)):
            partial.append(l2[i][l3[i]])
        result.append(partial)
        increment(l3, n)
    return result, l2, l1

def getX(p):
    p = p.decode()
    p = p.split("\n")

    for i in p:
        if len(i) != 0 and i[0] == "x":
            return float(i[2:])

def count_max(l, x):
    result = []
    for i in l:
        if i[0] == x:
            result.append(i[1])
    return max(result)


def configuration_count(l):
    result = []
    for i in l:
        if [i, 1] not in result:
            result.append([i, 1])
        elif [i, 1] in result:
            result.append([i, count_max(result, i) + 1])
    return result

def execute_gurobi(d, k, n):
    l, combi, all_points = all_pos(k, n)
    result = 0
    for q in l:
        print(q)
        count = 0
        q_unique = list(set(q))
        f = open("k+n_generating_file.py", "w+", encoding="utf-8")
        f.truncate(0)
        f.write("import gurobipy as gp\nfrom gurobipy import GRB\nimport math\n\n")
        f.write("m = gp.Model(\"qp\")\n\n")
        f.write("x = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"x\")\n\n")
        for i in range (1, k+ n + 1):
            for j in range(1, d + 1):
                f.write(
                    "p" + str(i) + str(j) + " = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"p" + str(i) + str(
                        j) + "\")\n")
            f.write("\n")
        f.write("\n\n")

        for i in q_unique:
            for k1 in range(1, q.count(i) + 1):
                for j in range(1, d + 1):
                    f.write(
                        "v" + str(i) + str(j) +str(k1)+ " = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"v" + str(
                            i) + str(
                            j) + str(k1) + "\")\n")
            f.write("\n")
        f.write("\n")

        f.write("m.setObjective(x, GRB.MAXIMIZE)\n\n")

        f.write("m.addConstr(p" + str(max(all_points)) + "1==1, \"res1\")")

        f.write("\n")

        for i in range(len(all_points)-1):
            f.write("m.addConstr(p" + str(all_points[i]) + "1<=p" + str(all_points[i+1]) + "1, \"c" + str(count) + "\")\n")
            count += 1

        f.write("\n")

        for i in q_unique:
            for j in range (1, q.count(i)+1):
                f.write("m.addConstr(p" + str(i) + str(1) + "*v" + str(i) + str(1) + str(j))
                for k1 in range(2, d + 1):
                    f.write("+p" + str(i) + str(k1) + "*v" + str(i) + str(k1) + str(j))
                f.write("==1, \"c" + str(count) + "\")\n")
                count += 1
            f.write("\n")


        for i in range (len(configuration_count(q))):
            for k1 in all_points:
                if k1 not in combi[i]:
                    f.write("m.addConstr(1")
                    for h in range(1, d + 1):
                        f.write("-p" + str(k1) + str(h) + "*v" + str(configuration_count(q)[i][0]) + str(h) + str(configuration_count(q)[i][1]))
                    f.write(">=x, \"c" + str(count) + "\")\n")
                    count += 1
        f.write("\n")

        f.write("\n")

        f.write("m.Params.NonConvex = 2\n\n")

        f.write("m.optimize()\n\n")

        f.write("for v in m.getVars():\n")

        f.write("\tprint('%s %g' % (v.varName, v.x))\n\n")

        f.close()

        if platform.system() == "Windows":
            p = subprocess.check_output("gurobi.bat k+n_generating_file.py", shell=True)
            if getX(p) > result:
                result = getX(p)
            print(result)
        elif platform.system() == "Linux":
            p = subprocess.check_output("gurobi.sh k+n_generating_file.py", shell=True)
            if getX(p) > result:
                result = getX(p)
            print(result)

    return result


def main():
    d = input("What is the value of d?\n")
    while d.isdigit() == False:
        print('Please input a positive integer.\n')
        d = input("What is the value of d?\n")

    k = input("What is the value of k?\n")
    while k.isdigit() == False and k >= d:
        print('Please input a positive integer.\n')
        d = input("What is the value of k?\n")

    n = input("What is the value of n?\n")
    while n.isdigit() == False:
        print('Please input a positive integer.\n')
        d = input("What is the value of n?\n")

    print("Final result:", execute_gurobi(int(d), int(k), int(n)))


main()
