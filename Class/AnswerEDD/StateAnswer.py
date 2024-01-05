
class StateAnswer():
   '''
   Estructura de datos que almacena los estados posibles que se entregan como 
   respuesta en la función transition_function de la clase AbstractProblem.
   '''

   def  __init__(self, value, feasibility, probability):
      '''
      Constructor de la clase StateAnswer 

      Parámetros:
      - value(): Valor del estado, debe seguir el tipo de datos utilizado anteriormente
      - feasibility(Bool): Indica si el estado es factible o no.
      - probability(int): Valor que representa la probabilidad de llegar a ese estado desde 
        el estado entregado en la función transition_function, para el valor de una variable 
        especifica.
      '''
      
      self.value = value
      self.feasibility = feasibility
      self.probability = probability
