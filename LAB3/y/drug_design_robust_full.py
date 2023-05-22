from pulp import *
import numpy as np

prob = LpProblem("The Drug production Problem", LpMinimize)

# Variables
r1 = LpVariable("RawI", 0)
r2 = LpVariable("RawII", 0)
d1 = LpVariable("DrugI", 0)
d2 = LpVariable("DrugII", 0)

# dual variables following procedure
Ud = 8
D1 = np.array([[1, 0, 0, 0], [-1, 0, 0, 0], [0, 1, 0, 0], [0, -1, 0, 0],
              [0, 0, 1, 0], [0, 0, -1, 0], [0, 0, 0, 1], [0, 0, 0, -1]])
d = np.array([-0.00995, 0.0105, -0.0196, 0.0204, 0.5, -0.5, 0.6, -0.6]).T
p1 = LpVariable.dicts(name='p1', indexs=range(Ud), lowBound=0)

# The objective function is added to 'prob' first
prob += (100 * r1 + 199.9 * r2+700*d1+800*d2) - \
    (6200*d1+6900*d2), "Negative of profit"

# 1. the first constraint is multiplied by -1 to become <= and fit lecture form
# 2. then we write robust counterpart (range vars must be bounded <=,>=, constant vars == constraint
# substituted with two <=, >= ---> all constraints changed to <=)
# 3. dualize and substitute as in the lecture
prob += lpSum([p1[i]*d[i] for i in range(Ud)]) <= 0, "Dualized1"

prob += lpSum([p1[i]*D1[i, 0] for i in range(Ud)]) == r1, "Dualized for RawI"
prob += lpSum([p1[i]*D1[i, 1] for i in range(Ud)]) == r2, "Dualized for RawII"
prob += lpSum([p1[i]*D1[i, 2] for i in range(Ud)]) == d1, "Dualized for DrugI"
prob += lpSum([p1[i]*D1[i, 3] for i in range(Ud)]) == d2, "Dualized for DrugII"

# four deterministic constraints
prob += r1+r2 <= 1000, "StorageConstraint"
prob += 90 * d1 + 100 * d2 <= 2000, "ManpowerConstraint"
prob += 40*d1+50*d2 <= 800, "EquipmentConstraint"
prob += 100 * r1 + 199.9 * r2 + 700*d1+800*d2 <= 10**5, "BudgetConstraint"

prob.solve()

print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print("Total negative profit = ", value(prob.objective))
