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
        Entregra la probabilidad de que un camino sea factible.
        '''

        nodes_probability = [-1 for i in range(len(self._graph.nodes))]
        nodes_probability[0] = 1

        for node in self._graph.nodes[1:]:
            id_node = int(node.id_node)
            nodes_probability[id_node] = 0
            
            for arc in node.in_arcs:
                if self._path[arc.variable_id] == arc.variable_value:
                    nodes_probability[id_node] += arc.probability * nodes_probability[int(arc.out_node.id_node)]
                nodes_probability[id_node] = round(nodes_probability[id_node], 3)

        return nodes_probability[-1]

