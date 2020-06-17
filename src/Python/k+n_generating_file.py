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

p51 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p51")
p52 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p52")



v111 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v111")
v121 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v121")
v112 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v112")
v122 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v122")
v113 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v113")
v123 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v123")

v211 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v211")
v221 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v221")
v212 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v212")
v222 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v222")

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

m.addConstr(p51==1, "res1")
m.addConstr(p11<=p21, "c0")
m.addConstr(p21<=p31, "c1")
m.addConstr(p31<=p41, "c2")
m.addConstr(p41<=p51, "c3")

m.addConstr(p11*v111+p12*v121==1, "c4")
m.addConstr(p11*v112+p12*v122==1, "c5")
m.addConstr(p11*v113+p12*v123==1, "c6")

m.addConstr(p21*v211+p22*v221==1, "c7")
m.addConstr(p21*v212+p22*v222==1, "c8")

m.addConstr(p31*v311+p32*v321==1, "c9")
m.addConstr(p31*v312+p32*v322==1, "c10")

m.addConstr(p41*v411+p42*v421==1, "c11")
m.addConstr(p41*v412+p42*v422==1, "c12")
m.addConstr(p41*v413+p42*v423==1, "c13")

m.addConstr(1-p31*v111-p32*v121>=x, "c14")
m.addConstr(1-p41*v111-p42*v121>=x, "c15")
m.addConstr(1-p51*v111-p52*v121>=x, "c16")
m.addConstr(1-p21*v311-p22*v321>=x, "c17")
m.addConstr(1-p41*v311-p42*v321>=x, "c18")
m.addConstr(1-p51*v311-p52*v321>=x, "c19")
m.addConstr(1-p21*v112-p22*v122>=x, "c20")
m.addConstr(1-p31*v112-p32*v122>=x, "c21")
m.addConstr(1-p51*v112-p52*v122>=x, "c22")
m.addConstr(1-p21*v113-p22*v123>=x, "c23")
m.addConstr(1-p31*v113-p32*v123>=x, "c24")
m.addConstr(1-p41*v113-p42*v123>=x, "c25")
m.addConstr(1-p11*v211-p12*v221>=x, "c26")
m.addConstr(1-p41*v211-p42*v221>=x, "c27")
m.addConstr(1-p51*v211-p52*v221>=x, "c28")
m.addConstr(1-p11*v411-p12*v421>=x, "c29")
m.addConstr(1-p31*v411-p32*v421>=x, "c30")
m.addConstr(1-p51*v411-p52*v421>=x, "c31")
m.addConstr(1-p11*v212-p12*v222>=x, "c32")
m.addConstr(1-p31*v212-p32*v222>=x, "c33")
m.addConstr(1-p41*v212-p42*v222>=x, "c34")
m.addConstr(1-p11*v412-p12*v422>=x, "c35")
m.addConstr(1-p21*v412-p22*v422>=x, "c36")
m.addConstr(1-p51*v412-p52*v422>=x, "c37")
m.addConstr(1-p11*v312-p12*v322>=x, "c38")
m.addConstr(1-p21*v312-p22*v322>=x, "c39")
m.addConstr(1-p41*v312-p42*v322>=x, "c40")
m.addConstr(1-p11*v413-p12*v423>=x, "c41")
m.addConstr(1-p21*v413-p22*v423>=x, "c42")
m.addConstr(1-p31*v413-p32*v423>=x, "c43")


m.Params.NonConvex = 2

m.optimize()

for v in m.getVars():
	print('%s %g' % (v.varName, v.x))

