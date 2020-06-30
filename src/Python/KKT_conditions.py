import gurobipy as gp
from gurobipy import GRB
from gurobipy import *

m = gp.Model("qp")

x = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="x")

m11 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="m12")
m12 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="m13")
m21 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="m21")
m22 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="m23")
m31 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="m31")
m32 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="m32")

l1 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="l1")
l2 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="l2")
l3 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="l3")

v11 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v11")
v12 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v12")

v21 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v21")
v22 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v22")

v31 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v31")
v32 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v32")


p11 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p11")
p12 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p12")

p21 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p21")
p22 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p22")

p31 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p31")
p32 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p32")


a12 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="a12")
a22 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="a22")
a32 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="a32")
a42 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="a42")
a52 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="a52")
a62 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="a62")


m.setObjective(x, GRB.MAXIMIZE)

m.addConstr(p11 <= p21, "00")
m.addConstr(p21 <= p31, "01")

m.addConstr(1-p21*v11-p22*v12>=x, "c211")
m.addConstr(1-p31*v11-p32*v12>=x, "c311")
m.addConstr(1-p11*v21-p12*v22>=x, "c122")
m.addConstr(1-p31*v21-p32*v22>=x, "c322")
m.addConstr(1-p11*v31-p12*v32>=x, "c133")
m.addConstr(1-p21*v31-p22*v32>=x, "c233")

m.addConstr(a12 == 1-p21*v11-p22*v12-x, "24")
m.addConstr(a22 == 1-p31*v11-p32*v12-x, "25")
m.addConstr(a32 == 1-p11*v21-p12*v22-x, "26")
m.addConstr(a42 == 1-p31*v21-p32*v22-x, "27")
m.addConstr(a52 == 1-p11*v31-p12*v32-x, "28")
m.addConstr(a62 == 1-p21*v31-p22*v32-x, "29")

m.addConstr(m12+m13+m21+m23+m31+m32 == 1, "1")

m.addConstr(l1*v11 == m21*v21+m31*v31, "2")
m.addConstr(l1*v12 == m21*v22+m31*v32, "3")
m.addConstr(l2*v21 == m12*v11+m32*v31, "4")
m.addConstr(l2*v22 == m12*v12+m32*v32, "5")
m.addConstr(l3*v31 == m13*v11+m23*v21, "6")
m.addConstr(l3*v32 == m13*v12+m23*v22, "7")

m.addConstr(l1*p11 == m21*p21+m31*p31, "8")
m.addConstr(l1*p12 == m21*p22+m31*p32, "9")
m.addConstr(l2*p21 == m12*p11+m32*p31, "10")
m.addConstr(l2*p22 == m12*p12+m32*p32, "11")
m.addConstr(l3*p31 == m13*p11+m23*p21, "12")
m.addConstr(l3*p32 == m13*p12+m23*p22, "13")

m.addConstr(p11*v11+p12*v12 == 1, "14")
m.addConstr(p21*v21+p22*v22 == 1, "15")
m.addConstr(p31*v31+p32*v32 == 1, "16")

m.addConstr(m12*a12 == 0, "30")
m.addConstr(m13*a22 == 0, "31")
m.addConstr(m21*a32 == 0, "32")
m.addConstr(m23*a42 == 0, "33")
m.addConstr(m31*a52 == 0, "34")
m.addConstr(m32*a62 == 0, "35")

m.Params.NonConvex = 2
m.Params.PoolSearchMode = 2
m.Params.PoolSolutions = 15

m.optimize()

print("All Solutions:")
for i in range (0, m.SolCount):
	print("\nSolution "+ str(i+1) + ":")
	m.Params.SolutionNumber = i
	print(m.PoolObjVal)
	for v in m.getVars():
		print('%s %g' % (v.varName, v.xn))
