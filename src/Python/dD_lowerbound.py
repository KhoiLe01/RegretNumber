import gurobipy as gp
from gurobipy import GRB

m = gp.Model("qp")

x = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="x")

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



m.setObjective(x, GRB.MAXIMIZE)


m.addConstr(p11<=p21, "c01")
m.addConstr(p21<=p31, "c02")


m.addConstr(p11*v11+p12*v12==1, "c11")
m.addConstr(1-p21*v11-p22*v12>=x, "c13")
m.addConstr(1-p31*v11-p32*v12>=x, "c14")

m.addConstr(p21*v21+p22*v22==1, "c21")
m.addConstr(1-p11*v21-p12*v22>=x, "c22")
m.addConstr(1-p31*v21-p32*v22>=x, "c24")

m.addConstr(p31*v31+p32*v32==1, "c31")
m.addConstr(1-p11*v31-p12*v32>=x, "c32")
m.addConstr(1-p21*v31-p22*v32>=x, "c33")


m.Params.NonConvex = 2
m.Params.PoolSearchMode = 2
m.Params.PoolSolutions = 15

m.optimize()

print("All Solutions:")
for i in range (0, m.SolCount):
	print("\nSolution "+ str(i+1))
	m.Params.SolutionNumber = i
	print(m.PoolObjVal)
	for v in m.getVars():
		print('%s %g' % (v.varName, v.xn))

