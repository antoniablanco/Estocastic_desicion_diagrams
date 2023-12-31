from abc import ABC, abstractmethod


class AbstractProblem(ABC):
    '''
    Esta clase ofrece una interfaz para que los usuarios puedan implementar sus 
    propias clases Problem. Las cuales pueden utilizar con la clase proporcionada DD 
    para resolver diagramas de decisión.

    *IMPORTANTE: Siempre que se hable de state tiene que seguir el mismo tipo que el entregado
    en initial_state.
    '''

    def __init__(self, initial_state, variables, values):
        '''
        Constructor de la clase AbstractProblem.

        Parámetros:
        - initial_state (NOT DEFINE): El estado inicial del problema, puede ser una lista, int,
        string, etc. Según lo que se requiera para el problema.
        - variables (list<tuple<variable, dominio>>): Una lista de tuplas que contiene las
        variables del problema y su dominio.
        - values (dict): Un diccionario que mapea variables a sus posibles valores con sus probabilidades

        Atributos:
        - initial_state (NOT DEFINE): El estado inicial del problema. *LEER IMPORTANTE.
        - ordered_variables (list): Lista de variables ordenadas.
        - variables_domain (dict): Diccionario que mapea variables a su dominio.
        '''
        self.initial_state = initial_state
        self.ordered_variables = self._get_variables(variables)
        self.variables_domain = dict(variables)
        self.values = values
    
    def _get_variables(self, variablesAndDomain):
        ''' 
        Obtiene una lista de variables ordenadas las cuales se obtienen del parametro variables.
        '''
        ordered_variables = []
        for var in variablesAndDomain:
            ordered_variables.append(var[0])
        return ordered_variables

    @abstractmethod
    def equals(self, state_one, state_two):
        '''
        Método abstracto que debe ser implementado por las subclases para determinar si dos estados son iguales.

        Parámetros:
        state_one: El primer estado a comparar. *LEER IMPORTANTE
        state_two: El segundo estado a comparar. *LEER IMPORTANTE

        Retorna:
        bool: True si los estados son iguales, False en caso contrario.
        '''
        raise NotImplementedError("The method equals has not been implemented yet")

    @abstractmethod
    def transition_function(self, previus_state, variable_id, variable_value):
        '''
        Método abstracto que debe ser implementado por las subclases para definir la función de transición.

        Parámetros:
        previus_state: El estado anterior. *LEER IMPORTANTE
        variable_id: El identificador de la variable que se modifica, sigue el mismo type que el entregado en 
        variables.
        variable_value: El valor de la variable que se modifica, es el valor posible de su dominio que se selecciono.

        Retorna:
        tuple: Una tupla que contiene el nuevo estado, siguiente el tipo entregado en inicial_state y un 
        isFeasible, que es True si el estado es factible, y False en caso contrario.
        '''
        raise NotImplementedError("The method transition_function has not been implemented yet")

    @abstractmethod
    def _probabilistic_function(self, variable_id, variable_value):
        '''
        Método abstracto que debe ser implementado por las subclases para definir la función probabilistica.

        Parámetros:
        variable_id: El identificador de la variable que se modifica, sigue el mismo type que el entregado en 
        variables.
        variable_value: El valor de la variable que se modifica, es el valor posible de su dominio que se selecciono.

        Retorna:
        dict: Un diccionario que mapea los valores posibles de la variable a su probabilidad.
        '''
        raise NotImplementedError("The method _probabilistic_function has not been implemented yet")