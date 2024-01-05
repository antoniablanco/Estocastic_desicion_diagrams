import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
root_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(root_dir)

from Class.EstocasticDD import EstocasticDD 
from IndependentSetProblem import ProblemIndependentSet
from Exceptions.MyExceptions import SameLenError

DictVecinos = {  'x_1': {2: 1, 3: 1, 4: 0.1},
            'x_2': {1: 1, 3: 0.9, 4: 1},
            'x_3': {1: 1, 2: 0.9, 4: 0.8, 5: 0.2},
            'x_4': {1: 0.1, 2: 1, 3: 0.8},
            'x_5': {3: 0.2}}
                
initial_state = [1, 2, 3, 4, 5]
variables = [('x_1', [0, 1]), ('x_2', [0, 1]), ('x_3', [0, 1]), ('x_4', [0, 1]), ('x_5', [0, 1])]

problem_instance = ProblemIndependentSet(initial_state, variables, DictVecinos)

dd_instance = EstocasticDD(problem_instance, verbose=False)
dd_instance.print_decision_diagram()

dd_instance.export_graph_file("estocastic_file")