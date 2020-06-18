import gurobipy as gp
from gurobipy import GRB

m = gp.Model("qp")

x = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="x")

v11 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v11")
v12 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v12")
v13 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v13")

v21 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v21")
v22 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v22")
v23 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v23")

v31 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v31")
v32 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v32")
v33 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v33")

v41 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v41")
v42 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v42")
v43 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v43")


p11 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p11")
p12 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p12")
p13 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p13")

p21 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p21")
p22 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p22")
p23 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p23")

p31 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p31")
p32 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p32")
p33 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p33")

p41 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p41")
p42 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p42")
p43 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p43")



m.setObjective(x, GRB.MAXIMIZE)


m.addConstr(p11<=p21, "c01")
m.addConstr(p21<=p31, "c02")
m.addConstr(p31<=p41, "c03")


m.addConstr(p11*v11+p12*v12+p13*v13==1, "c11")
m.addConstr(1-p21*v11-p22*v12-p23*v13>=x, "c13")
m.addConstr(1-p31*v11-p32*v12-p33*v13>=x, "c14")
m.addConstr(1-p41*v11-p42*v12-p43*v13>=x, "c15")

m.addConstr(p21*v21+p22*v22+p23*v23==1, "c21")
m.addConstr(1-p11*v21-p12*v22-p13*v23>=x, "c22")
m.addConstr(1-p31*v21-p32*v22-p33*v23>=x, "c24")
m.addConstr(1-p41*v21-p42*v22-p43*v23>=x, "c25")

m.addConstr(p31*v31+p32*v32+p33*v33==1, "c31")
m.addConstr(1-p11*v31-p12*v32-p13*v33>=x, "c32")
m.addConstr(1-p21*v31-p22*v32-p23*v33>=x, "c33")
m.addConstr(1-p41*v31-p42*v32-p43*v33>=x, "c35")

m.addConstr(p41*v41+p42*v42+p43*v43==1, "c41")
m.addConstr(1-p11*v41-p12*v42-p13*v43>=x, "c42")
m.addConstr(1-p21*v41-p22*v42-p23*v43>=x, "c43")
m.addConstr(1-p31*v41-p32*v42-p33*v43>=x, "c44")


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

