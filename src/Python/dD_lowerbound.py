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

v51 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v51")
v52 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v52")
v53 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v53")

v61 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v61")
v62 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v62")
v63 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v63")

v71 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v71")
v72 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v72")
v73 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="v73")


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

p61 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p61")
p62 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p62")
p63 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p63")

p71 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p71")
p72 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p72")
p73 = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name="p73")



m.setObjective(x, GRB.MAXIMIZE)


m.addConstr(p11<=p21, "c01")
m.addConstr(p21<=p31, "c02")
m.addConstr(p31<=p41, "c03")
m.addConstr(p41<=p51, "c04")
m.addConstr(p51<=p61, "c05")
m.addConstr(p61<=p71, "c06")


m.addConstr(p11*v11+p12*v12+p13*v13==1, "c11")
m.addConstr(1-p21*v11-p22*v12-p23*v13>=x, "c13")
m.addConstr(1-p31*v11-p32*v12-p33*v13>=x, "c14")
m.addConstr(1-p41*v11-p42*v12-p43*v13>=x, "c15")
m.addConstr(1-p51*v11-p52*v12-p53*v13>=x, "c16")
m.addConstr(1-p61*v11-p62*v12-p63*v13>=x, "c17")
m.addConstr(1-p71*v11-p72*v12-p73*v13>=x, "c18")

m.addConstr(p21*v21+p22*v22+p23*v23==1, "c21")
m.addConstr(1-p11*v21-p12*v22-p13*v23>=x, "c22")
m.addConstr(1-p31*v21-p32*v22-p33*v23>=x, "c24")
m.addConstr(1-p41*v21-p42*v22-p43*v23>=x, "c25")
m.addConstr(1-p51*v21-p52*v22-p53*v23>=x, "c26")
m.addConstr(1-p61*v21-p62*v22-p63*v23>=x, "c27")
m.addConstr(1-p71*v21-p72*v22-p73*v23>=x, "c28")

m.addConstr(p31*v31+p32*v32+p33*v33==1, "c31")
m.addConstr(1-p11*v31-p12*v32-p13*v33>=x, "c32")
m.addConstr(1-p21*v31-p22*v32-p23*v33>=x, "c33")
m.addConstr(1-p41*v31-p42*v32-p43*v33>=x, "c35")
m.addConstr(1-p51*v31-p52*v32-p53*v33>=x, "c36")
m.addConstr(1-p61*v31-p62*v32-p63*v33>=x, "c37")
m.addConstr(1-p71*v31-p72*v32-p73*v33>=x, "c38")

m.addConstr(p41*v41+p42*v42+p43*v43==1, "c41")
m.addConstr(1-p11*v41-p12*v42-p13*v43>=x, "c42")
m.addConstr(1-p21*v41-p22*v42-p23*v43>=x, "c43")
m.addConstr(1-p31*v41-p32*v42-p33*v43>=x, "c44")
m.addConstr(1-p51*v41-p52*v42-p53*v43>=x, "c46")
m.addConstr(1-p61*v41-p62*v42-p63*v43>=x, "c47")
m.addConstr(1-p71*v41-p72*v42-p73*v43>=x, "c48")

m.addConstr(p51*v51+p52*v52+p53*v53==1, "c51")
m.addConstr(1-p11*v51-p12*v52-p13*v53>=x, "c52")
m.addConstr(1-p21*v51-p22*v52-p23*v53>=x, "c53")
m.addConstr(1-p31*v51-p32*v52-p33*v53>=x, "c54")
m.addConstr(1-p41*v51-p42*v52-p43*v53>=x, "c55")
m.addConstr(1-p61*v51-p62*v52-p63*v53>=x, "c57")
m.addConstr(1-p71*v51-p72*v52-p73*v53>=x, "c58")

m.addConstr(p61*v61+p62*v62+p63*v63==1, "c61")
m.addConstr(1-p11*v61-p12*v62-p13*v63>=x, "c62")
m.addConstr(1-p21*v61-p22*v62-p23*v63>=x, "c63")
m.addConstr(1-p31*v61-p32*v62-p33*v63>=x, "c64")
m.addConstr(1-p41*v61-p42*v62-p43*v63>=x, "c65")
m.addConstr(1-p51*v61-p52*v62-p53*v63>=x, "c66")
m.addConstr(1-p71*v61-p72*v62-p73*v63>=x, "c68")

m.addConstr(p71*v71+p72*v72+p73*v73==1, "c71")
m.addConstr(1-p11*v71-p12*v72-p13*v73>=x, "c72")
m.addConstr(1-p21*v71-p22*v72-p23*v73>=x, "c73")
m.addConstr(1-p31*v71-p32*v72-p33*v73>=x, "c74")
m.addConstr(1-p41*v71-p42*v72-p43*v73>=x, "c75")
m.addConstr(1-p51*v71-p52*v72-p53*v73>=x, "c76")
m.addConstr(1-p61*v71-p62*v72-p63*v73>=x, "c77")


m.Params.NonConvex = 2

m.optimize()

for v in m.getVars():
	print('%s %g' % (v.varName, v.x))