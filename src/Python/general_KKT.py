import os
import sys
import platform

def kkt(k, d, sol_count):
    f = open("KKT_conditions.py", "r+")
    f.truncate(0)
    f.write("import gurobipy as gp\nfrom gurobipy import GRB\n\n")
    f.write("m = gp.Model(\"qp\")\n\n")
    f.write("x = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"x\")\n\n")

	# add mu variables to Gurobi model
    for i in range (1,k+2):
		for j in range (1,d+1):
			f.write("m"+str(i)+str(j)+" = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"m"+str(i)+str(j)+"\")\n")
		f.write("\n")
	f.write("\n")

	# add lambda variables to Gurobi model
    for i in range (1,k+2):
		f.write("l"+str(i)+" = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"l"+str(i)+"\")\n")

	# add utility variables to Gurobi model
    for i in range (1,k+2):
        for j in range (1,d+1):
            f.write("v"+str(i)+str(j)+" = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"v"+str(i)+str(j)+"\")\n")
        f.write("\n")
    f.write("\n")

	# add point variables to Gurobi model
    for i in range (1,k+2):
        for j in range (1,d+1):
            f.write("p"+str(i)+str(j)+" = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"p"+str(i)+str(j)+"\")\n")
        f.write("\n")

	# add a variables to Gurobi model
	for i in range (1,k+2):
        for j in range (1,d+1):
            f.write("a"+str(i)+str(j)+" = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"p"+str(i)+str(j)+"\")\n")
        f.write("\n")
    f.write("\n\n")

	# set Gurobi model to maximize objective function
    f.write("m.setObjective(x, GRB.MAXIMIZE)\n\n\n")

	# variable to count constraints
	count = 0

	# add constraint to sort points
    for i in range (1, k+1):
        f.write("m.addConstr(p"+str(i)+"1<=p"+str(i+1)+"1, \"c"+str(count)+"\")\n")
		count += 1

    f.write("\n\n")

	# dot product == 1
    for i in range (1,k+2):
        f.write("m.addConstr(p"+str(i)+str(1)+"*v"+str(i)+str(1))
        for j in range (2,d+1):
            f.write("+p"+str(i)+str(j)+"*v"+str(i)+str(j))
        f.write("==1, \"c"+str(count)+"\")\n")
		count += 1
    f.write("\n")

	f.write("m.addConstr(1")
	for i in range(1,k+2):
		for j in range(1,d+1):
			f.write("-p" + str() + "*v" + str(i) + str(j) )
	f.write(">=x, \"c" + str(count) + "\")\n")
	count += 1
	f.write("\n")

    f.write("\n")

    f.write("m.Params.NonConvex = 2\n")
    f.write("m.Params.PoolSearchMode = 2\n")
    f.write("m.Params.PoolSolutions = "+str(sol_count)+"\n\n")

    f.write("m.optimize()\n\n")

    f.write("print(\"All Solutions:\")\n")
    f.write("for i in range (0, m.SolCount):\n")
    f.write("\tprint(\"\\nSolution \"+ str(i+1))\n")
    f.write("\tm.Params.SolutionNumber = i\n")
    f.write("\tprint(m.PoolObjVal)\n")
    f.write("\tfor v in m.getVars():\n")
    f.write("\t\tprint('%s %g' % (v.varName, v.xn))\n\n")

    f.write("")

    f.close()


def main():
    d = input("What is the value of d?\n")
    while d.isdigit() == False:
        print('Please input a positive integer.\n')
        d = input("What is the value of d?\n")

    k = input("What is the value of k?\n")
    while k.isdigit() == False or int(k) < int(d):
        print('Please input a positive integer that is >= d.\n')
        k = input("What is the value of k?\n")

    sol_count = input("How many solutions should be computed?\n")
    while sol_count.isdigit() == False:
        print('Please input a positive integer.\n')
        sol_count = input("How many solutions should be computed?\n")

    kkt(int(k), int(d), int(sol_count))
    if platform.system() == "Windows":
        os.system("gurobi.bat KKT_conditions.py")
    elif platform.system() == "Linux":
        os.system("gurobi.sh KKT_conditions.py")

main()
