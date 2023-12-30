import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

sys.path.append(parent_dir)

from Class.EstocasticDD import EstocasticDD 
from ExampleProblem import ProblemKnapsack
from Exceptions.MyExceptions import SameLenError

# Valores construcción knapsack
matrix_of_wheight = [3, 3, 4, 6]
right_side_of_restrictions = 5

# Valores construcción abstract problem
initial_state = [0]
variables = [('x_1', [0, 1]), ('x_2', [0, 1]), ('x_3', [0, 1]), ('x_4', [0, 1])]

problem_instance = ProblemKnapsack(initial_state, variables, matrix_of_wheight, right_side_of_restrictions)

dd_instance = EstocasticDD(problem_instance, verbose=True)
dd_instance.print_decision_diagram()

dd_instance.export_graph_file("estocastic_file")

