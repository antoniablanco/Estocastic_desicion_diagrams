from Class.EstocasticDDBuilder.EstocasticDDBuilder import EstocasticDDBuilder
from Class.ReduceEstocasticDDBuilder.ReduceEstocasticDDBuilder import ReduceDDBuilder
from Class.GraphVisualization.Print import Print
from Class.GraphVisualization.GraphFile import GraphFile
from Class.EstocasticDDStructure.Node import Node
from Class.EstocasticDDStructure.Arc import Arc
from Class.EstocasticDDStructure.Graph import Graph
from Class.Problems.AbstractProblemClass import AbstractProblem
from Class.Algorithms.PathProbability import PathProbability
import copy
import time

class EstocasticDD():
    '''
    Clase DD (Decision Diagram) para la creación y manipulación de diagramas de decisión.
    '''
    def __init__(self, problem: AbstractProblem, verbose=False):
        '''
        Constructor de la clase DD.

        Parámetros:
        problem: Una instancia de la clase problem, que se utilizará para crear el diagrama de decisión.

        Atributos:
        - problem: Una instancia de la clase problem, que se utilizará para crear el diagrama de decisión.
        - graph_DD: El diagrama de decisión creado, que se actualiza al generar el diagrama reducido o relajado.
        '''
        self.estocastic_dd_builder_time = 0
        self.reduce_estocastic_dd_builder_time = 0

        self.problem = problem
        self.graph_DD = self._create_estocastic_decision_diagram(verbose)

    def _create_estocastic_decision_diagram(self, verbose: bool) -> Graph:
        '''
        Método privado que crea el diagrama de decisión estocastico.

        Parámetros:
        verbose (bool): Si es True, se imprime la construcción del grafo.
        '''
        print("")
        print("Iniciando la creación del diagrama de decision estocastico...")
        start_time = time.time()  
        self.estocastic_dd_builder = EstocasticDDBuilder(self.problem)
        graph = self.estocastic_dd_builder.get_decision_diagram(verbose)
        end_time = time.time()  
        self.estocastic_dd_builder_time = end_time - start_time

        print(f"Diagrama de decision estocastico creado")
        return graph
    
    def reduce_estocastic_decision_diagram(self, verbose: bool) -> Graph:
        '''
        Método privado que crea el diagrama de decisión estocastico reducido.

        Parámetros:
        verbose (bool): Si es True, se imprime la construcción del grafo.
        '''
        print("")
        print("Iniciando la reducción del diagrama de decision estocastico...")
        start_time = time.time()  
        self.reduce_estocastic_dd_builder = ReduceDDBuilder(self.graph_DD)
        self.graph_DD = self.reduce_estocastic_dd_builder.get_reduce_decision_diagram(verbose)
        end_time = time.time()  
        self.reduce_estocastic_dd_builder_time = end_time - start_time

        print(f"Diagrama de decision estocastico reducido")

    
    def print_decision_diagram(self) -> None:
        '''
        NOTA: Este método es solo para fines de prueba, y es importante tener en cuenta que posee 
        máximo 4 tipos de lineas diferente.
        '''
        print_instance = Print(self.graph_DD)
        return print_instance.print_graph_G()

    def export_graph_file(self, file_name: str) -> None:
        '''
        Genera un archivo .GML con el diagrama de decisión actual.

        Parámetros:
        file_name (str): El nombre del archivo Margarita.

        Retorna:
        None
        '''
        GraphFile(file_name, self.graph_DD)

    def get_decision_diagram_graph(self) -> Graph:
        ''' Retorna un objeto de la clase Graph. '''
        return self.graph_DD

    def get_decision_diagram_graph_copy(self) -> Graph:
        ''' Retorna una copia del objeto de la clase Graph, que no posee un
        puntero al mismo objeto. '''
        return copy.deepcopy(self.graph_DD)
    
    def get_path_probability(self, path: dict) -> float:
        '''
        Retorna la probabilidad de ocurrencia de un camino.

        Parámetros:
        path (dict): Diccionar con los id de las variables como llaves y 
                     los valores de las variables como valores.

        Retorna:
        float: La probabilidad de ocurrencia del camino.
        '''
        
        self.check_path(path)

        start_time = time.time()  
        path_probability = PathProbability(self.graph_DD, path)
        probability = path_probability.get_path_probability()
        end_time = time.time()  
        path_probability_time = end_time - start_time

        print()
        print(f'La probabilidad de ocurrencia del camino {path} es: {probability} y se demoro {round(path_probability_time, 5)} segundos')

        return probability
    
    def check_path(self, path: dict) -> None:
        '''
        Verifica que el camino sea válido.

        Parámetros:
        path (dict): Diccionar con los id de las variables como llaves y 
                     los valores de las variables como valores.

        Retorna:
        None
        '''
        for key in path.keys():
            if key not in self.problem.ordered_variables:
                raise Exception(f'La variable {key} no se encuentra entre las variables del diagrama de decision')
            if path[key] not in self.problem.variables_domain[key]:
                raise Exception(f'El valor {path[key]} no se encuentra en el dominio de la variable {key}')

    def get_estocastic_dd_time(self) -> float:
        ''' Retorna el tiempo de ejecución de create_estocastic_decision_diagram. '''
        return self.estocastic_dd_builder_time
    
    def get_reduce_estocastic_dd_time(self) -> float:
        ''' Retorna el tiempo de ejecución de reduce_estocastic_decision_diagram. '''
        return self.reduce_estocastic_dd_builder_time