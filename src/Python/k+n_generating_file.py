import gurobipy as gp
from gurobipy import GRB
import math

m = gp.Model("qp")

x = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="x")

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

p51 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p51")
p52 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p52")
p53 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p53")



v111 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v111")
v121 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v121")
v131 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v131")
v112 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v112")
v122 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v122")
v132 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v132")
v113 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v113")
v123 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v123")
v133 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v133")

v311 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v311")
v321 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v321")
v331 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v331")
v312 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v312")
v322 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v322")
v332 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v332")
v313 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v313")
v323 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v323")
v333 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v333")

v411 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v411")
v421 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v421")
v431 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v431")
v412 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v412")
v422 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v422")
v432 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v432")

v511 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v511")
v521 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v521")
v531 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v531")
v512 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v512")
v522 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v522")
v532 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v532")


m.setObjective(x, GRB.MAXIMIZE)

m.addConstr(p51==1, "res1")
m.addConstr(p11<=p21, "c0")
m.addConstr(p21<=p31, "c1")
m.addConstr(p31<=p41, "c2")
m.addConstr(p41<=p51, "c3")

m.addConstr(p11*v111+p12*v121+p13*v131==1, "c4")
m.addConstr(p11*v112+p12*v122+p13*v132==1, "c5")
m.addConstr(p11*v113+p12*v123+p13*v133==1, "c6")

m.addConstr(p31*v311+p32*v321+p33*v331==1, "c7")
m.addConstr(p31*v312+p32*v322+p33*v332==1, "c8")
m.addConstr(p31*v313+p32*v323+p33*v333==1, "c9")

m.addConstr(p41*v411+p42*v421+p43*v431==1, "c10")
m.addConstr(p41*v412+p42*v422+p43*v432==1, "c11")

m.addConstr(p51*v511+p52*v521+p53*v531==1, "c12")
m.addConstr(p51*v512+p52*v522+p53*v532==1, "c13")

m.addConstr(1-p31*v111-p32*v121-p33*v131>=x, "c14")
m.addConstr(1-p41*v111-p42*v121-p43*v131>=x, "c15")
m.addConstr(1-p51*v111-p52*v121-p53*v131>=x, "c16")
m.addConstr(1-p21*v112-p22*v122-p23*v132>=x, "c17")
m.addConstr(1-p41*v112-p42*v122-p43*v132>=x, "c18")
m.addConstr(1-p51*v112-p52*v122-p53*v132>=x, "c19")
m.addConstr(1-p21*v113-p22*v123-p23*v133>=x, "c20")
m.addConstr(1-p31*v113-p32*v123-p33*v133>=x, "c21")
m.addConstr(1-p51*v113-p52*v123-p53*v133>=x, "c22")
m.addConstr(1-p21*v511-p22*v521-p23*v531>=x, "c23")
m.addConstr(1-p31*v511-p32*v521-p33*v531>=x, "c24")
m.addConstr(1-p41*v511-p42*v521-p43*v531>=x, "c25")
m.addConstr(1-p11*v311-p12*v321-p13*v331>=x, "c26")
m.addConstr(1-p41*v311-p42*v321-p43*v331>=x, "c27")
m.addConstr(1-p51*v311-p52*v321-p53*v331>=x, "c28")
m.addConstr(1-p11*v411-p12*v421-p13*v431>=x, "c29")
m.addConstr(1-p31*v411-p32*v421-p33*v431>=x, "c30")
m.addConstr(1-p51*v411-p52*v421-p53*v431>=x, "c31")
m.addConstr(1-p11*v512-p12*v522-p13*v532>=x, "c32")
m.addConstr(1-p31*v512-p32*v522-p33*v532>=x, "c33")
m.addConstr(1-p41*v512-p42*v522-p43*v532>=x, "c34")
m.addConstr(1-p11*v312-p12*v322-p13*v332>=x, "c35")
m.addConstr(1-p21*v312-p22*v322-p23*v332>=x, "c36")
m.addConstr(1-p51*v312-p52*v322-p53*v332>=x, "c37")
m.addConstr(1-p11*v313-p12*v323-p13*v333>=x, "c38")
m.addConstr(1-p21*v313-p22*v323-p23*v333>=x, "c39")
m.addConstr(1-p41*v313-p42*v323-p43*v333>=x, "c40")
m.addConstr(1-p11*v412-p12*v422-p13*v432>=x, "c41")
m.addConstr(1-p21*v412-p22*v422-p23*v432>=x, "c42")
m.addConstr(1-p31*v412-p32*v422-p33*v432>=x, "c43")


m.Params.NonConvex = 2

m.optimize()

for v in m.getVars():
	print('%s %g' % (v.varName, v.x))

