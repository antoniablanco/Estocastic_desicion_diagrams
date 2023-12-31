from Class.EstocasticDDBuilder.EstocasticDDBuilder import EstocasticDDBuilder
from Class.GraphVisualization.Print import Print
from Class.GraphVisualization.GraphFile import GraphFile
import copy
import time

class EstocasticDD():
    '''
    Clase DD (Decision Diagram) para la creación y manipulación de diagramas de decisión.
    '''
    def __init__(self, problem, verbose=False):
        '''
        Constructor de la clase DD.

        Parámetros:
        problem: Una instancia de la clase problem, que se utilizará para crear el diagrama de decisión.

        Atributos:
        - problem: Una instancia de la clase problem, que se utilizará para crear el diagrama de decisión.
        - graph_DD: El diagrama de decisión creado, que se actualiza al generar el diagrama reducido o relajado.
        '''
        self.estocastic_dd_builder_time = 0

        self.problem = problem
        self.graph_DD = self._create_estocastic_decision_diagram(verbose)

    def _create_estocastic_decision_diagram(self, verbose):
        print("")
        print("Iniciando la creación del diagrama de decision estocastico...")
        start_time = time.time()  
        self.estocastic_dd_builder = EstocasticDDBuilder(self.problem)
        graph = self.estocastic_dd_builder.get_decision_diagram(verbose)
        end_time = time.time()  
        self.estocastic_dd_builder_time = end_time - start_time

        print(f"Diagrama de decision estocastico creado")
        return graph
    
    def print_decision_diagram(self):
        '''
        NOTA: Este método es solo para fines de prueba, y es importante tener en cuenta que posee 
        máximo 4 tipos de lineas diferente.
        '''
        print_instance = Print(self.graph_DD)
        return print_instance.print_graph_G()

    def export_graph_file(self, file_name):
        '''
        Genera un archivo .GML con el diagrama de decisión actual.

        Parámetros:
        file_name (str): El nombre del archivo Margarita.

        Retorna:
        None
        '''
        GraphFile(file_name, self.graph_DD)

    def get_decision_diagram_graph(self):
        ''' Retorna un objeto de la clase Graph. '''
        return self.graph_DD

    def get_decision_diagram_graph_copy(self):
        ''' Retorna una copia del objeto de la clase Graph, que no posee un
        puntero al mismo objeto. '''
        return copy.deepcopy(self.graph_DD)
    
    def get_estocasticDDBuilder_time(self):
        ''' Retorna el tiempo de ejecución del EstocasticDDBuilder. '''
        return self.estocastic_dd_builder_time