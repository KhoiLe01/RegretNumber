import gurobipy as gp
from gurobipy import GRB
import math

m = gp.Model("qp")

x = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="x")

p11 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p11")
p12 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p12")
p13 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p13")
p14 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p14")

p21 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p21")
p22 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p22")
p23 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p23")
p24 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p24")

p31 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p31")
p32 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p32")
p33 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p33")
p34 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p34")

p41 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p41")
p42 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p42")
p43 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p43")
p44 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p44")

p51 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p51")
p52 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p52")
p53 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p53")
p54 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p54")



v111 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v111")
v121 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v121")
v131 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v131")
v141 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v141")

v211 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v211")
v221 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v221")
v231 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v231")
v241 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v241")

v311 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v311")
v321 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v321")
v331 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v331")
v341 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v341")

v411 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v411")
v421 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v421")
v431 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v431")
v441 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v441")

v511 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v511")
v521 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v521")
v531 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v531")
v541 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v541")


m.setObjective(x, GRB.MAXIMIZE)

m.addConstr(p51==1, "res1")
m.addConstr(p11<=p21, "c0")
m.addConstr(p21<=p31, "c1")
m.addConstr(p31<=p41, "c2")
m.addConstr(p41<=p51, "c3")

m.addConstr(p11*v111+p12*v121+p13*v131+p14*v141==1, "c4")

m.addConstr(p21*v211+p22*v221+p23*v231+p24*v241==1, "c5")

m.addConstr(p31*v311+p32*v321+p33*v331+p34*v341==1, "c6")

m.addConstr(p41*v411+p42*v421+p43*v431+p44*v441==1, "c7")

m.addConstr(p51*v511+p52*v521+p53*v531+p54*v541==1, "c8")

m.addConstr(1-p21*v111-p22*v121-p23*v131-p24*v141>=x, "c9")
m.addConstr(1-p31*v111-p32*v121-p33*v131-p34*v141>=x, "c10")
m.addConstr(1-p41*v111-p42*v121-p43*v131-p44*v141>=x, "c11")
m.addConstr(1-p51*v111-p52*v121-p53*v131-p54*v141>=x, "c12")
m.addConstr(1-p11*v211-p12*v221-p13*v231-p14*v241>=x, "c13")
m.addConstr(1-p31*v211-p32*v221-p33*v231-p34*v241>=x, "c14")
m.addConstr(1-p41*v211-p42*v221-p43*v231-p44*v241>=x, "c15")
m.addConstr(1-p51*v211-p52*v221-p53*v231-p54*v241>=x, "c16")
m.addConstr(1-p11*v311-p12*v321-p13*v331-p14*v341>=x, "c17")
m.addConstr(1-p21*v311-p22*v321-p23*v331-p24*v341>=x, "c18")
m.addConstr(1-p41*v311-p42*v321-p43*v331-p44*v341>=x, "c19")
m.addConstr(1-p51*v311-p52*v321-p53*v331-p54*v341>=x, "c20")
m.addConstr(1-p11*v411-p12*v421-p13*v431-p14*v441>=x, "c21")
m.addConstr(1-p21*v411-p22*v421-p23*v431-p24*v441>=x, "c22")
m.addConstr(1-p31*v411-p32*v421-p33*v431-p34*v441>=x, "c23")
m.addConstr(1-p51*v411-p52*v421-p53*v431-p54*v441>=x, "c24")
m.addConstr(1-p11*v511-p12*v521-p13*v531-p14*v541>=x, "c25")
m.addConstr(1-p21*v511-p22*v521-p23*v531-p24*v541>=x, "c26")
m.addConstr(1-p31*v511-p32*v521-p33*v531-p34*v541>=x, "c27")
m.addConstr(1-p41*v511-p42*v521-p43*v531-p44*v541>=x, "c28")


m.Params.NonConvex = 2

m.optimize()

for v in m.getVars():
	print('%s %g' % (v.varName, v.x))

