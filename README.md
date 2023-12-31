# Estocastic Decision Diagram Program

This program provides a versatile implementation of Estocastic Decision Graphs for solving optimization problems. The following guide will help you use the program.

## Requisites

Make sure you have in your system

* python > 3.11
* networkx
* matplotlibsd

For a complete use of the program, it is recommended to have a tool that can read documents with a .gml extension. yED is a suitable program for this purpose.

## Installation

Clone this repository and navigate to the project directory to implement the main program. To review examples, go to the '/Examples/' directory, where you'll find three folders with different examples. In each of them, execute the one with 'main' at the end of its name.

## Getting Started

First should proceed to the construction of a **Problem** class, which must inherit from  **AbstractProblem** . It is crucial to define the following functions for this class:

* **equals:** Takes two states as input and should give as output a boolean value indicating whether they are equal or not.
* **transition_function:** Takes as inputs a previous state, a variable identifier (e.g., "x_2"), and the domain this variable takes (e.g., "1"). It outputs a new state and a boolean value indicating whether the state is feasible or not.
* **_probabilistic_function**: Based on the ID of a variable and its associated value, a dictionary is provided where each key represents a possible state, and the corresponding value is its probability of occurrence.

Once this class is built, it is essential to create an instance of it to be passed to the "EstocasticDD" class. In this, you'll find functions to create, reduce and visualize a diagram, as well as obtain a copy of it.

## Features

#### Create Estocastic Decision Diagram

It is the initial and necessary feature for all the following ones; that's why it is included when creating an instance of the EstocasticDD class. To do this, you need to provide an instance of the created Problem class.

#### Create Reduce Decision

To create the reduced decision diagram, is necesary use *create_reduce_estocastic_decision_diagram()* from the **EstocasticDD** class, which transforms the graph class object saved when creating the diagram into its reduced form. This new version is then stored within the **Estocastic****DD** class.

#### Print Decision Diagram

For a quick visualization of the created diagram, can be use the *print_decision_diagram()* method of the **EstocasticDD** class. It's important to note that this method uses the networkx library; therefore, it has a limitation of 5 different line types. If you have a variable domain greater than this, the design of the arcs will be repeated.

#### Export Decision Diagram

To export the created decision diagram, whether it's reduced or in its original format, should be use the *export_graph_file()* method of the **EstocasticDD** class. This generates a *.gml* file that can be visualized in programs such as *yED.*

#### Get a Copy Of the Decision Diagram

To obtain a copy of the **EstocasticDD** instance without it being a pointer to the original object, you should use the *get_decision_diagram_graph_copy()* method of the **EstocasticDD** class. This feature can be useful for testing different constructors or functions to solve the diagram.

#### Get the Time of the Algoritms

If it's want to get the time taken by the algorithms for creating the diagram or another of its forms, you need to use the *get_estocasticDDBuilder_time()* or *get_zzz_constructor_time()* methods of the **EstocasticDD** class, where zzz represent the type of graph that its wnated, for example reduce. 

## Examples

For a more comprehensive understanding of these classes, it is recommended to thoroughly review the examples available in the **"/Examples/"** folder within the code, and execute **Knapsack/KnapsackMain** *or* **IndependentSet/IndependentSetMain.** These examples are generic and open for testing different values. In light of the above, the examples will be explained below.

#### Knapsack

Within the **KnapsackMain** file, it can be noticed that it is a generalized version of a linear problem. For this reason, it is possible to input the weights of the variables in the different constraints. This should be done in the *matrix_of_weight* parameter, and it is also necessary to provide the value on the right side of the constraints in the *right_side_of_restrictions* parameter. With these two values, an instance of Knapsack can be created. However, to generate a decision diagram, it is necessary to provide the initial state in *initial_state* and the variables with their domain in *variables.* After defining all the parameters and delivering them in the creation of an instance of the KnapsackProblem, it is ready to test the various features that were explained earlier. Importantly, it should be noted that there are some checks in place to ensure there is no inconsistency in the provided data.

#### IndependentSet

Similar to the previous case, it can be observed that in the IndependentSetMain file, it corresponds to a generalization of the IndependentSet problem. Therefore, it is possible to test different values. To do so, it is necessary to provide a dictionary in which the *key* is the variable's ID, and the *value* corresponds to a list of all nodes, that can be reached in a single arc, formatted as integers. Once the variables are selected to instantiate the IndependentSet, it is necessary to create the variables to build a decision diagram. These include *initial_state* on one hand and, on the other hand, the variable IDs with their domain in *variables.* After providing all the parameters to the instance of the constructed problem class, you can test the other features.

## Extending the Code

It is important to emphasize that all classes along with their modules have been documented for a more detailed understanding. This can be useful if it's want to create new objective functions or diagram constructors, which are expected to follow the same directory structure.
