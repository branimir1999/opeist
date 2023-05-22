from pulp import *

prob = LpProblem("The Drug production Problem", LpMinimize)

# Variables
r1 = LpVariable("RawI", 0)
r2 = LpVariable("RawII", 0)
d1 = LpVariable("DrugI", 0)
d2 = LpVariable("DrugII", 0)

# The objective function is added to 'prob' first
prob += (100 * r1 + 199.9 * r2+700*d1+800*d2)-(6200*d1+6900*d2), "Negative of profit"

# The five constraints are entered
prob += 0.01*r1 + 0.02*r2-0.5*d1-0.6*d2>=0, "BalanceOfActiveAgent"
prob += r1+r2 <= 1000, "StorageConstraint"
prob += 90 * d1 + 100 * d2 <= 2000, "ManpowerConstraint"
prob += 40*d1+50*d2<=800, "EquipmentConstraint"
prob += 100 * r1 + 199.9 * r2 + 700*d1+800*d2 <= 10**5, "BudgetConstraint"

prob.solve()

print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print("Total negative profit = ", value(prob.objective))
