from pulp import *

tjedni_plan = LpProblem("Proizvodnja_grickalica", LpMaximize) # Maksimizacija profita
x1 = LpVariable("Grickalica 1", 0, None, LpInteger) # Grickalica 1 je x1
x2 = LpVariable("Grickalica 2", 0, None, LpInteger) # Grickalica 2 je x2
x3 = LpVariable("Grickalica 3", 0, None, LpInteger) # Grickalica 3 je x3
tjedni_plan += 4*x1 + 4.5*x2 + 3.5*x3 # Funkcija cilja tj z odnosno profit
tjedni_plan += 0.125*x1 + 0.15*x2 + 0.1*x3 <= 40, "vrijeme_proizvodnje" # Ogranicenje vremena proizvodnje stroja
tjedni_plan += 0.5*x1 + 0.5*x2 + 0.5*x3 <= 150, "prostor_grickalica" # Ogranicenje prostora za vrećice
tjedni_plan.solve() # Softverski riješi
for grickalica in tjedni_plan.variables(): # Ispiši rezultat
    print(grickalica.name, ":", grickalica.varValue)

tjedni_plan_d = LpProblem("Proizvodnja_grickalica_dual", LpMinimize) # Minimizacija u dualu
y1 = LpVariable("y1", 0, None, LpInteger)
y2 = LpVariable("y2", 0, None, LpInteger)
tjedni_plan_d += 40*y1 + 150*y2
tjedni_plan_d += 0.125*y1 + 0.5*y2 >= 4, "vrijednost x1"
tjedni_plan_d += 0.15*y1 + 0.5*y2 >= 4.5, "vrijednost x2"
tjedni_plan_d += 0.1*y1 + 0.5*y2 >= 3.5, "vrijednost x3"
tjedni_plan_d.solve() # Softverski riješi
for grickalica in tjedni_plan_d.variables(): # Ispiši rezultat
    print(grickalica.name, ":", grickalica.varValue)
