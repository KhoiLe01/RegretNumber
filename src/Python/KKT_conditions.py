import gurobipy as gp
from gurobipy import GRB

m = gp.Model("qp")

x = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="x")

l1 = m.addVar(lb= -1, ub= 1, vtype=GRB.CONTINUOUS, name="l1")

m12 = m.addVar(lb= 0, ub= 10, vtype=GRB.CONTINUOUS, name="m12")
m13 = m.addVar(lb= 0, ub= 10, vtype=GRB.CONTINUOUS, name="m13")
l2 = m.addVar(lb= -1, ub= 1, vtype=GRB.CONTINUOUS, name="l2")

m21 = m.addVar(lb= 0, ub= 10, vtype=GRB.CONTINUOUS, name="m21")
m23 = m.addVar(lb= 0, ub= 10, vtype=GRB.CONTINUOUS, name="m23")
l3 = m.addVar(lb= -1, ub= 1, vtype=GRB.CONTINUOUS, name="l3")

m31 = m.addVar(lb= 0, ub= 10, vtype=GRB.CONTINUOUS, name="m31")
m32 = m.addVar(lb= 0, ub= 10, vtype=GRB.CONTINUOUS, name="m32")

p11 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p11")
v11 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v11")
p12 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p12")
v12 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v12")

p21 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p21")
v21 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v21")
p22 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p22")
v22 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v22")

p31 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p31")
v31 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v31")
p32 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p32")
v32 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v32")

a12 = m.addVar(lb= 0, ub= 10, vtype=GRB.CONTINUOUS, name="a12")
a13 = m.addVar(lb= 0, ub= 10, vtype=GRB.CONTINUOUS, name="a13")
a21 = m.addVar(lb= 0, ub= 10, vtype=GRB.CONTINUOUS, name="a21")
a23 = m.addVar(lb= 0, ub= 10, vtype=GRB.CONTINUOUS, name="a23")
a31 = m.addVar(lb= 0, ub= 10, vtype=GRB.CONTINUOUS, name="a31")
a32 = m.addVar(lb= 0, ub= 10, vtype=GRB.CONTINUOUS, name="a32")

m.setObjective(x, GRB.MAXIMIZE)

m.addConstr(p11<=p21, "0")
m.addConstr(p21<=p31, "1")

m.addConstr(1-p21*v11-p22*v12>=x, "2")
m.addConstr(a12 == 1-p21*v11-p22*v12-x, "3")
m.addConstr(1-p31*v11-p32*v12>=x, "4")
m.addConstr(a13 == 1-p31*v11-p32*v12-x, "5")
m.addConstr(1-p11*v21-p12*v22>=x, "6")
m.addConstr(a21 == 1-p11*v21-p12*v22-x, "7")
m.addConstr(1-p31*v21-p32*v22>=x, "8")
m.addConstr(a23 == 1-p31*v21-p32*v22-x, "9")
m.addConstr(1-p11*v31-p12*v32>=x, "10")
m.addConstr(a31 == 1-p11*v31-p12*v32-x, "11")
m.addConstr(1-p21*v31-p22*v32>=x, "12")
m.addConstr(a32 == 1-p21*v31-p22*v32-x, "13")

m.addConstr(m12+m13+m21+m23+m31+m32 == 1, "14")

m.addConstr(l1*v11 == m21*v21+m31*v31, "15")
m.addConstr(l1*p11 == m21*p21+m31*p31, "16")
m.addConstr(l1*v12 == m21*v22+m31*v32, "17")
m.addConstr(l1*p12 == m21*p22+m31*p32, "18")
m.addConstr(l2*v21 == m12*v11+m32*v31, "19")
m.addConstr(l2*p21 == m12*p11+m32*p31, "20")
m.addConstr(l2*v22 == m12*v12+m32*v32, "21")
m.addConstr(l2*p22 == m12*p12+m32*p32, "22")
m.addConstr(l3*v31 == m13*v11+m23*v21, "23")
m.addConstr(l3*p31 == m13*p11+m23*p21, "24")
m.addConstr(l3*v32 == m13*v12+m23*v22, "25")
m.addConstr(l3*p32 == m13*p12+m23*p22, "26")

m.addConstr(p11*v11+p12*v12 == 1, "27")
m.addConstr(p21*v21+p22*v22 == 1, "28")
m.addConstr(p31*v31+p32*v32 == 1, "29")

m.addConstr(m12*a12 == 0, "30")
m.addConstr(m13*a13 == 0, "31")
m.addConstr(m21*a21 == 0, "32")
m.addConstr(m23*a23 == 0, "33")
m.addConstr(m31*a31 == 0, "34")
m.addConstr(m32*a32 == 0, "35")

m.Params.NonConvex = 2
m.Params.PoolSearchMode = 2
m.Params.PoolSolutions = 5

m.optimize()

print("All Solutions:")
for i in range (0, m.SolCount):
	print("\nSolution "+ str(i+1))
	m.Params.SolutionNumber = i
	print(m.PoolObjVal)
	for v in m.getVars():
		print('%s %g' % (v.varName, v.xn))

