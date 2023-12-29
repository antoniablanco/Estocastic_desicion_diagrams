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

dd_instance = EstocasticDD(problem_instance, verbose=False)
dd_instance.print_decision_diagram()

dd_instance.export_graph_file("estocastic_test")

'''
import matplotlib.pyplot as plt
import networkx as nx

G = nx.DiGraph()
edge_list = [(1,2,{'w':'A1'}),(2,1,{'w':'A2'}),(2,3,{'w':'B'}),(3,1,{'w':'C'}),
             (3,4,{'w':'D1'}),(4,3,{'w':'D2'}),(1,5,{'w':'E1'}),(5,1,{'w':'E2'}),
             (3,5,{'w':'F'}),(5,4,{'w':'G'})]
G.add_edges_from(edge_list)
pos=nx.spring_layout(G,seed=4)
fig, ax = plt.subplots()
nx.draw_networkx_nodes(G, pos, ax=ax)
nx.draw_networkx_labels(G, pos, ax=ax)

curved_edges = [edge for edge in G.edges() if reversed(edge) in G.edges()]
straight_edges = list(set(G.edges()) - set(curved_edges))
nx.draw_networkx_edges(G, pos, ax=ax, edgelist=straight_edges)
arc_rad = 0.25
nx.draw_networkx_edges(G, pos, ax=ax, edgelist=curved_edges, connectionstyle=f'arc3, rad = {arc_rad}')

fig.savefig("3.png", bbox_inches='tight',pad_inches=0)
'''