import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

root_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))

sys.path.append(root_dir)

from Class.EstocasticDD import EstocasticDD 
from KnapsackProblem import ProblemKnapsack
from Exceptions.MyExceptions import SameLenError

# Valores construcción knapsack
matrix_of_wheight = [[3, 3, 4, 6]]
right_side_of_restrictions = [5]
values = {
            0 : [{0:1},
                 {0:1},
                 {0:1},
                 {0:1}],

            1 : [{1: 0.5, 2: 0.5},
                 {2: 0.3, 3: 0.7},
                 {1: 0.4, 4: 0.6},
                 {3: 0.9, 4: 0.1} ]
                }

# Valores construcción abstract problem
initial_state = [0]
variables = [('x_1', [0, 1]), ('x_2', [0, 1]), ('x_3', [0, 1]), ('x_4', [0, 1])]

problem_instance = ProblemKnapsack(initial_state, variables, matrix_of_wheight, right_side_of_restrictions, values)

dd_instance = EstocasticDD(problem_instance, verbose=False)
dd_instance.print_decision_diagram()

dd_instance.export_graph_file("estocastic_file")

