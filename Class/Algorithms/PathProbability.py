import copy
from Class.EstocasticDDStructure.Graph import Graph

class PathProbability():
    '''
    Clase que implementa un algoritmo para la reducción de un grafo de decisión.
    '''

    def __init__(self, graph: Graph, path: list):
        '''
        Algortimo para saber la probabilidad de ocurrencia de un camino entregado.

        Parámetros:
        - graph (Graph): El grafo de decisión en el cual se trabaja.
        - path (list): Lista de nodos que conforman el camino.
        '''
        
        self._graph = copy.deepcopy(graph)
        self._path = path

    def get_path_probability(self):
        '''
        Entregra la probabilidad de ocurrencia del camino entregado.
        '''
        return 0.8
