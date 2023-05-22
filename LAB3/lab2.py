from pulp import *
import numpy as np

def construct_problem(costs: np.ndarray) -> LpProblem:
    model = LpProblem("Problem_Pridruzivanja", LpMinimize)
    matrix_range = [*range(costs.shape[0])] # Lista prvih n prirodnih brojeva gdje je n dimenzija matrice "costs"
    x = LpVariable.dicts(name="x", indexs=(matrix_range,matrix_range), lowBound=0, upBound=1, cat=LpBinary)
        
    model += lpSum([costs[i][j] * x[i][j] for i in matrix_range for j in matrix_range]), "Funkcija cilja"
    
    # Ako pretpostavimo da je [i][j] == (x,y)
    for i in matrix_range:
        model += lpSum([x[i][j] for j in matrix_range]) == 1, "Stupac " + str(i)
    for j in matrix_range:
        model += lpSum([x[i][j] for i in matrix_range]) == 1, "Redak" + str (j)
          
    return model

def solve_LP(model: LpProblem) -> None:
    model.solve(PULP_CBC_CMD(msg=0))
    
def solve_CP(model: LpProblem) -> None:
    model.solve(PULP_CHOCO_CMD(msg=0))

matrix_size = 8
jmbag_seed = 3651686321
np.random.seed(jmbag_seed)

mali_costs = np.random.randint(low=1, high=21, size=(matrix_size, matrix_size))
veliki_costs = np.random.randint(low=1, high=21, size=(matrix_size*2, matrix_size*2))
