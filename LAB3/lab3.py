from pulp import *
import numpy as np
from typing import Tuple

def construct_LP_equivalent() -> Tuple[LpProblem, dict]:
    # Problem
    model = LpProblem("Robust_LP", LpMaximize)

    # Varijable
    x1 = LpVariable(name="x1", lowBound=0, upBound=None, cat=LpContinuous)
    x2 = LpVariable(name="x2", lowBound=0, upBound=None, cat=LpContinuous)

    # Interval pouzdanosti
    # alfa - beta >= 0
    # alfa - beta <= 2
    # alfa + beta >= 4
    # alfa + beta <= 6
    #(Pretvaramo sve u manje-jednako) =>
    # -alfa + beta <= 0
    # alfa - beta  <= 2
    # -alfa - beta <= -4
    # alfa + beta  <= 6

    # Dualne varijable
    Ud = 4
    D1 = np.array([[-1, 1], [1, -1], [-1, -1], [1, 1]])
    d = np.array([0, 2, 4, 6]).T
    p1 = LpVariable.dicts(name='p1', indexs=range(Ud), lowBound=0, upBound=None, cat=LpContinuous)

    # Funkcija cilja i ogranicenja na glavne varijable
    model += (3*x1 + 5*x2), "Criteria_Function"
    model += x1 <= 4, "x1_constraint"
    model += x2 <= 6, "x2_constraint"
    model += lpSum([p1[i]*d[i] for i in range(Ud)]) <= 18, "Dualized_optimiziation_constraint"

    # Dualizirana ogranicenja
    model += lpSum([p1[i]*D1[i, 0] for i in range(Ud)]) == x1, "Dualized_x1_constraint"
    model += lpSum([p1[i]*D1[i, 1] for i in range(Ud)]) == x2, "Dualized_x2_constraint"
    
    model.solve(PULP_CBC_CMD(msg=0))
    
    # Stvaramo dict bitnih varijabli
    variables_dict = dict()
    variables_dict["x1"] = x1
    variables_dict["x2"] = x2
    
    return model, variables_dict
