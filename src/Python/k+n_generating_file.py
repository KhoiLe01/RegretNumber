import gurobipy as gp
from gurobipy import GRB
import math

m = gp.Model("qp")

x = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="x")

p11 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p11")
p12 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p12")

p21 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p21")
p22 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p22")

p31 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p31")
p32 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p32")

p41 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p41")
p42 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p42")



v211 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v211")
v221 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v221")

v311 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v311")
v321 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v321")
v312 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v312")
v322 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v322")

v411 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v411")
v421 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v421")
v412 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v412")
v422 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v422")
v413 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v413")
v423 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v423")


m.setObjective(x, GRB.MAXIMIZE)

m.addConstr(p41==1, "res1")
m.addConstr(p11<=p21, "c0")
m.addConstr(p21<=p31, "c1")
m.addConstr(p31<=p41, "c2")

m.addConstr(p21*v211+p22*v221==1, "c3")

m.addConstr(p31*v311+p32*v321==1, "c4")
m.addConstr(p31*v312+p32*v322==1, "c5")

m.addConstr(p41*v411+p42*v421==1, "c6")
m.addConstr(p41*v412+p42*v422==1, "c7")
m.addConstr(p41*v413+p42*v423==1, "c8")

m.addConstr(1-p31*v211-p32*v221>=x, "c9")
m.addConstr(1-p41*v211-p42*v221>=x, "c10")
m.addConstr(1-p21*v311-p22*v321>=x, "c11")
m.addConstr(1-p41*v311-p42*v321>=x, "c12")
m.addConstr(1-p21*v411-p22*v421>=x, "c13")
m.addConstr(1-p31*v411-p32*v421>=x, "c14")
m.addConstr(1-p11*v312-p12*v322>=x, "c15")
m.addConstr(1-p41*v312-p42*v322>=x, "c16")
m.addConstr(1-p11*v412-p12*v422>=x, "c17")
m.addConstr(1-p31*v412-p32*v422>=x, "c18")
m.addConstr(1-p11*v413-p12*v423>=x, "c19")
m.addConstr(1-p21*v413-p22*v423>=x, "c20")


m.Params.NonConvex = 2

m.optimize()

for v in m.getVars():
	print('%s %g' % (v.varName, v.x))

