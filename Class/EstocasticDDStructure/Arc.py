
class Arc():
    '''
    Clase que representa una estructura de los arcos. 
    '''

    def __init__(self, out_node, in_node, variable_value, variable_id, probability):
        '''
        Constructor de la clase Arc.

        Parámetros:
        - out_node(Node): Nodo de salida del arco.
        - in_node(Node): Nodo de entrada del arco.
        - variable_value(int): Valor de la variable asociada al arco.
        - variable_id(string): Identificador único de la variable asociada al arco.
        '''
        self.out_node = out_node
        self.in_node = in_node
        self.variable_value = variable_value
        self.variable_id = variable_id
        self.probability = probability
    
    def __str__(self) -> str:
        '''
        Retorna:
        str: Representación de cadena del objeto Arc.
        '''
        return "arc_" + str(self.out_node.id_node) + "_" + str(self.in_node.id_node) + " "+str(self.probability)+"%"
    
    