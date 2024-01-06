import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Class.EstocasticDDStructure.Node import Node
from Class.EstocasticDDStructure.Arc import Arc
from Class.EstocasticDDStructure.Graph import Graph

node_0 = Node('0', [0])
graph = Graph(node_0)

### LAYER X_1
graph.new_layer()
node_1 = Node('1', [0])
arc_0_1 = Arc(node_0, node_1, 0, 'x_1', 1.0)
node_0.add_out_arc(arc_0_1)
node_1.add_in_arc(arc_0_1)
graph.add_node(node_1)

node_2 = Node('2', [1])
arc_0_2 = Arc(node_0, node_2, 1, 'x_1', 0.5)
node_0.add_out_arc(arc_0_2)
node_2.add_in_arc(arc_0_2)
graph.add_node(node_2)

node_3 = Node('3', [2])
arc_0_3 = Arc(node_0, node_3, 1, 'x_1', 0.5)
node_0.add_out_arc(arc_0_3)
node_3.add_in_arc(arc_0_3)
graph.add_node(node_3)

### LAYER X_2   
graph.new_layer()
node_4 = Node('4', [0])
arc_1_4 = Arc(node_1, node_4, 0, 'x_2', 1)
node_1.add_out_arc(arc_1_4)
node_4.add_in_arc(arc_1_4)
graph.add_node(node_4)

node_5 = Node('5', [2])
arc_1_5 = Arc(node_1, node_5, 1, 'x_2', 0.3)
arc_3_5 = Arc(node_3, node_5, 0, 'x_2', 1)
node_1.add_out_arc(arc_1_5)
node_3.add_out_arc(arc_3_5)
node_5.add_in_arc(arc_1_5)
node_5.add_in_arc(arc_3_5)
graph.add_node(node_5)

node_6 = Node('6', [3])
arc_1_6 = Arc(node_1, node_6, 1, 'x_2', 0.7)
arc_2_6 = Arc(node_2, node_6, 1, 'x_2', 1)
arc_3_6 = Arc(node_3, node_6, 1, 'x_2', 0.3)
node_1.add_out_arc(arc_1_6)
node_2.add_out_arc(arc_2_6)
node_3.add_out_arc(arc_3_6)
node_6.add_in_arc(arc_1_6)
node_6.add_in_arc(arc_2_6)
node_6.add_in_arc(arc_3_6)
graph.add_node(node_6)

node_7 = Node('7', [1])
arc_2_7 = Arc(node_2, node_7, 0, 'x_2', 1)
node_2.add_out_arc(arc_2_7)
node_7.add_in_arc(arc_2_7)
graph.add_node(node_7)

node_8 = Node('8', [5])
arc_3_8 = Arc(node_3, node_8, 1, 'x_2', 0.7)
node_3.add_out_arc(arc_3_8)
node_8.add_in_arc(arc_3_8)
graph.add_node(node_8)

### LAYER X_3
graph.new_layer()
node_9 = Node('9', [0])
arc_4_9_op1 = Arc(node_4, node_9, 0, 'x_3', 1)
arc_4_9_op2 = Arc(node_4, node_9, 1, 'x_3', 0.4)
arc_7_9 = Arc(node_7, node_9, 0, 'x_3', 1)
node_4.add_out_arc(arc_4_9_op1)
node_4.add_out_arc(arc_4_9_op2)
node_7.add_out_arc(arc_7_9)
node_9.add_in_arc(arc_4_9_op1)
node_9.add_in_arc(arc_4_9_op2)
node_9.add_in_arc(arc_7_9)
graph.add_node(node_9)

node_10 = Node('10', [4])
arc_4_10 = Arc(node_4, node_10, 1, 'x_3', 0.6)
arc_5_10 = Arc(node_5, node_10, 1, 'x_3', 0.4)
arc_6_10_op1 = Arc(node_6, node_10, 0, 'x_3', 1)
arc_6_10_op2 = Arc(node_6, node_10, 1, 'x_3', 0.4)
arc_7_10 = Arc(node_7, node_10, 1, 'x_3', 0.6)
arc_8_10 = Arc(node_8, node_10, 0, 'x_3', 1)
node_4.add_out_arc(arc_4_10)
node_5.add_out_arc(arc_5_10)
node_6.add_out_arc(arc_6_10_op1)
node_6.add_out_arc(arc_6_10_op2)
node_7.add_out_arc(arc_7_10)
node_8.add_out_arc(arc_8_10)
node_10.add_in_arc(arc_4_10)
node_10.add_in_arc(arc_5_10)
node_10.add_in_arc(arc_6_10_op1)
node_10.add_in_arc(arc_6_10_op2)
node_10.add_in_arc(arc_7_10)
node_10.add_in_arc(arc_8_10)
graph.add_node(node_10)

node_11 = Node('11', [2])
arc_5_11 = Arc(node_5, node_11, 0, 'x_3', 1)
arc_7_11 = Arc(node_7, node_11, 1, 'x_3', 0.4)
node_5.add_out_arc(arc_5_11)
node_7.add_out_arc(arc_7_11)
node_11.add_in_arc(arc_5_11)
node_11.add_in_arc(arc_7_11)
graph.add_node(node_11)

### LAYER X_4
graph.new_layer()

node_12 = Node('12', [0])
arc_9_12_op1 = Arc(node_9, node_12, 0, 'x_4', 1)
arc_9_12_op2 = Arc(node_9, node_12, 1, 'x_4', 1) 
arc_10_12 = Arc(node_10, node_12, 0, 'x_4', 1)
arc_11_12_op1 = Arc(node_11, node_12, 1, 'x_4', 0.9)
arc_11_12_op2 = Arc(node_11, node_12, 0, 'x_4', 1)

node_9.add_out_arc(arc_9_12_op1)
node_9.add_out_arc(arc_9_12_op2)
node_10.add_out_arc(arc_10_12)
node_11.add_out_arc(arc_11_12_op1)
node_11.add_out_arc(arc_11_12_op2)

node_12.add_in_arc(arc_9_12_op1)
node_12.add_in_arc(arc_9_12_op2)
node_12.add_in_arc(arc_10_12)
node_12.add_in_arc(arc_11_12_op1)
node_12.add_in_arc(arc_11_12_op2)
graph.add_node(node_12)