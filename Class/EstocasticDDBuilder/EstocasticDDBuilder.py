from Class.EstocasticDDStructure.Node import Node
from Class.EstocasticDDStructure.Arc import Arc
from Class.EstocasticDDStructure.Graph import Graph
from Class.Problems.AbstractProblemClass import AbstractProblem


class EstocasticDDBuilder():
    '''
    Clase que entrega el código base para la construcción de diagramas de decisión estocástico.
    '''

    def __init__(self, problem: AbstractProblem):
        '''
        Constructor de los diagramas estocásticos.

        Parámetros:
        - problem: Objeto tipo problema para el cual se construirá el grafo.
        '''
        self._node_number = 1
        self.graph = None

        self._problem = problem
        self._variables = problem.ordered_variables
        self._variables_domain = problem.variables_domain

        self._initialize_graph(problem.initial_state)
        
    def _initialize_graph(self, initial_state):
        '''
        Inicializa el grafo con un nodo raíz.

        Parámetros:
        - initial_state: Estado inicial del problema.
        '''
        node_root = Node(0, initial_state)
        self.graph = Graph(node_root)
    
    def get_decision_diagram(self, should_visualize: bool) -> Graph:
        '''
        Retorna el grafo de decisión construido.

        Parámetros:
        - should_visualize: Booleano que indica si se debe visualizar la construcción del grafo.

        Retorna:
        - Graph: Objeto tipo grafo de decisión construido.
        '''
        for variable_id in range(len(self._variables)):
            self._create_new_layer(variable_id)
            self._print_graph(should_visualize)

        return self.graph

    def _create_new_layer(self, variable_id: int):
        '''
        Crea una nueva capa en el grafo para una variable dada.

        Parámetros:
        - variable_id: Índice de la variable para la cual se crea la nueva capa.
        '''
        self.graph.new_layer()
        self._create_new_nodes_in_the_new_layer(variable_id)

    def _create_new_nodes_in_the_new_layer(self, variable_id: int):
        '''
        Crea nodos en la nueva capa del grafo.

        Parámetros:
        - variable_id: Índice de la variable para la cual se crean nodos en la nueva capa.
        '''
        for existed_node in self.graph.structure[-2][:]:
            for variable_value in self._variables_domain[self._variables[variable_id]]:
                self._check_if_new_node_should_be_created(variable_value, existed_node, variable_id)
    
    def _check_if_new_node_should_be_created(self, variable_value: int, existed_node: Node, variable_id: int):
        '''
        Lleva a cabo la creación de arcos y nodos si es necesario

        Parámetros:
        - variable_value: Valor de la variable para la cual se verifica la creación del nuevo nodo.
        - existed_node: Nodo existente en la capa anterior.
        - variable_id: Índice de la variable para la cual se realiza la verificación.
        '''
        states = self._problem.transition_function(existed_node.state, self._variables[variable_id], variable_value)

        for posible_state in states:
            if posible_state.feasibility:
                if self._there_is_node_in_last_layer(variable_id):
                    self._create_arcs_for_the_terminal_node(existed_node, variable_value, variable_id, posible_state.probability)
                else:
                    self._create_rest_of_arcs(existed_node, variable_value, variable_id, posible_state.value, posible_state.probability)
        
    def _there_is_node_in_last_layer(self, variable_id: int) -> bool:
        '''
        Verifica si hay nodos en la última capa del grafo.

        Parámetros:
        - variable_id: Índice de la variable para la cual se realiza la verificación.

        Retorna:
        bool: True si hay nodos en la última capa, False en caso contrario.
        '''
        return self._variables[-1] == self._variables[variable_id] and self.graph.structure[-1] != []
    
    def _create_arcs_for_the_terminal_node(self, existed_node: Node, variable_value: int, variable_id: int, probability: int):
        '''
        Crea arcos para el nodo terminal en la última capa.

        Parámetros:
        - existed_node: Nodo existente en la capa anterior.
        - variable_value: Valor de la variable para la cual se crean los arcos.
        - variable_id: Índice de la variable para la cual se crean los arcos.
        '''

        same_state_node = self.graph.structure[-1][-1]
        self._create_arc_for_node(existed_node, same_state_node, variable_value, variable_id, probability)
    
    def _create_rest_of_arcs(self, existed_node: Node, variable_value: int, variable_id: int, node_state, probability: int):
        '''
        Crea los arcos para un nodo que no se encuentra en la última capa.

        Parámetros:
        - existed_node: Nodo existente en la capa anterior.
        - variable_value: Valor de la variable para la cual se crean los arcos.
        - variable_id: Índice de la variable para la cual se crean los arcos.
        - node_state: Estado del nuevo nodo.
        '''
        exist_node, same_state_node = self._exist_node_with_same_state(node_state)
        if exist_node:
            self._create_arc_for_node(existed_node, same_state_node, variable_value, variable_id, probability)
        else:
            self._create_new_node_and_arc(existed_node, variable_value, variable_id, node_state, probability)

    def _exist_node_with_same_state(self, node_state) -> tuple:
        '''
        Verifica si existe un nodo con el mismo estado en la misma capa.

        Parámetros:
        - node_state: Estado del nodo para el cual se realiza la verificación.

        Retorna:
        tuple: (bool, Node) - True si existe un nodo con el mismo estado, False y None en caso contrario.
        '''
        for node in self.graph.structure[-1]:
            if self._problem.equals(node.state, node_state):
                return True, node
        return False, None

    def _create_new_node_and_arc(self, existed_node: Node, variable_value: int, variable_id: int, node_state, probability: int):
        '''
        Crea un nuevo nodo y un arco para un nodo ya existente.

        Parámetros:
        - existed_node: Nodo existente en la capa anterior.
        - variable_value: Valor de la variable para la cual se crea el arco.
        - variable_id: Índice de la variable para la cual se crea el arco.
        - node_state: Estado del nuevo nodo.
        '''
        node_created = Node(str(self._node_number), node_state)
        self._node_number += 1
        self._create_arc_for_node(existed_node, node_created, variable_value, variable_id, probability)
        self.graph.add_node(node_created)

    def _create_arc_for_node(self, out_node: Node, in_node: Node, variable_value: int, variable_id: int, probability: int):
        '''
        Crea un arco para un nodo ya existente.

        Parámetros:
        - existed_node: Nodo existente en la capa anterior.
        - node_created: Nuevo nodo creado.
        - variable_value: Valor de la variable para la cual se crea el arco.
        - variable_id: Índice de la variable para la cual se crea el arco.
        '''
        arc = Arc(out_node, in_node, variable_value, self._variables[variable_id], probability)
        out_node.add_out_arc(arc)
        in_node.add_in_arc(arc)

    def _print_graph(self, should_visualize: bool):
        '''
        Imprime el grafo si se solicita la visualización.

        Parámetros:
        - should_visualize: Booleano que indica si se debe visualizar el grafo.
        '''
        if should_visualize:
            self._print()
 
    def _print(self):
        '''
        Imprime el contenido de cada capa del grafo.
        '''
        print("")
        for layer in self.graph.structure:
            print("------------------------------------------------------")
            for node in layer:
                in_arcs_str = ", ".join(str(arc) for arc in node.in_arcs)
                print(str(node) + "(" + in_arcs_str + ")", end=" ")
            print("")
    