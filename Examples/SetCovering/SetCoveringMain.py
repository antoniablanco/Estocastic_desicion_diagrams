import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

root_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))

sys.path.append(root_dir)

from Class.EstocasticDD import EstocasticDD 
from SetCoveringProblem import SetCoveringProblem


# Valores construcción abstract problem
initial_state = [1, 2, 3]
variables = [('x_1', [0, 1]), ('x_2', [0, 1]), ('x_3', [0, 1]), ('x_4', [0, 1]), ('x_5', [0, 1])]

# Valores construcción Set covering problem
matrix_of_wheight = [[1, 1, 0.2, 0, 0],
                     [0.3, 0, 0, 0.4, 1],
                     [0, 1, 0.7, 0.6, 0]]

right_side_of_restrictions = [1, 1, 1]

problem_instance = SetCoveringProblem(initial_state, variables, matrix_of_wheight, right_side_of_restrictions)
dd_instance = EstocasticDD(problem_instance, verbose=False)

dd_instance.print_decision_diagram()
dd_instance.reduce_estocastic_decision_diagram(verbose=False)
dd_instance.print_decision_diagram()

graph = dd_instance.get_decision_diagram_graph()
dd_instance.export_graph_file("estocastic_file")

# Algoritmos
path = {'x_1': 0, 'x_2': 0, 'x_3': 1, 'x_4': 1, 'x_5': 1}
dd_instance.get_path_probability(path)
     