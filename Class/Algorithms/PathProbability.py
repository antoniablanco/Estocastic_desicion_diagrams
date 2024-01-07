import copy
from Class.EstocasticDDStructure.Graph import Graph

class PathProbability():
    '''
    Clase que implementa un algoritmo para la reducción de un grafo de decisión.
    '''

    def __init__(self, graph: Graph, path: dict):
        '''
        Algortimo para saber la probabilidad de ocurrencia de un camino entregado.

        Parámetros:
        - graph (Graph): El grafo de decisión en el cual se trabaja.
        - path (list): Lista de nodos que conforman el camino.
        '''
        
        self._graph = copy.deepcopy(graph)
        self._path = path

    def get_path_probability(self) -> float:
        '''
        Entregra la probabilidad de ocurrencia del camino entregado.
        '''
        self._clean_previous_weight()

        for layer in self._graph.structure[1:]:
            for node in layer:
                node.weight = 0
                for arc in node.in_arcs:
                    if self._path[arc.variable_id] == arc.variable_value:
                        node.weight += arc.probability * arc.out_node.weight
                node.weight = round(node.weight, 3)

        return self._graph.structure[-1][-1].weight
    
    def _clean_previous_weight(self):
        '''
        Método privado que limpia los pesos anteriores de los nodos.
        '''
        for node in self._graph.nodes:
            node.weight = 0

        self._graph.nodes[0].weight = 1
