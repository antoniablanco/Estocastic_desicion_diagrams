import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Class.Problems.AbstractProblemClass import AbstractProblem
from Class.AnswerEDD.StateAnswer import StateAnswer
from Exceptions.MyExceptions import SameVariables, MustBeIntegers, ConsistentDictionaryOfNeighbors

class ProblemIndependentSet(AbstractProblem):

    def __init__(self, initial_state, variables, dict_node_neighbors):
        super().__init__(initial_state, variables, dict_node_neighbors)
        self.dict_node_neighbors = dict_node_neighbors

        self.check_atributes(variables)

    def check_atributes(self, variables):
        self.check_same_variables(variables)
        self.check_neighbors_must_be_integers_and_in_range()
        self.check_consistent_dictionary_of_neighbors()

    def check_same_variables(self, variables):
        assert dict(variables).keys() == self.dict_node_neighbors.keys(), "Variables must be the same between dictionaries"
    
    def check_neighbors_must_be_integers_and_in_range(self):
        for key in self.dict_node_neighbors.keys():
            for neighbor_key, value in self.dict_node_neighbors.get(key, {}).items():
                if not (isinstance(neighbor_key, int) and 0 <= value <= 1):
                    raise ValueError(f"Invalid entry for node {key}: Neighbor key must be an integer, and value must be in the range [0, 1]. Got neighbor {neighbor_key} with value {value}.")
    
    def check_consistent_dictionary_of_neighbors(self):
        for key, neighbors in self.dict_node_neighbors.items():
            for neighbor_key, _ in neighbors.items():
                if int(key[2:]) not in self.dict_node_neighbors.get("x_" + str(neighbor_key), {}):
                    raise ValueError(f"Dictionary of neighbors must be consistent. Node {key} is connected to Node x_{neighbor_key}, but the reverse connection is missing.")

    def equals(self, state_one, state_two):
        return set(state_one) == set(state_two)

    def transition_function(self, previus_state, variable_id, variable_value):
        statesList = []
        
        if int(variable_value) == 0 and int(variable_id[2:]) in previus_state:
            new_state = previus_state.copy()
            new_state.remove(int(variable_id[2:]))
            state_answer = StateAnswer(new_state, True, 1)
            statesList.append(state_answer)
            
        elif int(variable_value) == 0 and int(variable_id[2:]) not in previus_state:
            state_answer = StateAnswer(previus_state.copy(), True, 1)
            statesList.append(state_answer)

        elif int(variable_value) == 1 and int(variable_id[2:]) in previus_state:
            static_state = previus_state.copy()
            static_state.remove(int(variable_id[2:]))
            possible_neighbors = []

            neighbors = self._probabilistic_function(variable_id)
            for key in neighbors.keys():
                if key in static_state:
                    static_state.remove(key)
                    possible_neighbors.append(key)

            for bitset in range(1<<len(possible_neighbors)):
                new_state = static_state.copy()
                probability = 1
                isFeasible = True
                for i in range(len(possible_neighbors)):
                    if bitset & (1<<i):
                        if neighbors[possible_neighbors[i]] == 0: 
                            isFeasible = False
                            probability = 0
                        else:
                            probability *= neighbors[possible_neighbors[i]]
                    else:
                        new_state.append(possible_neighbors[i])
                        if neighbors[possible_neighbors[i]] == 1: 
                            isFeasible = False
                            probability = 0
                        else:
                            probability *= (1 - neighbors[possible_neighbors[i]])

                probability = round(probability, 3)
                new_state.sort()
                state_answer = StateAnswer(new_state, isFeasible, probability)
                statesList.append(state_answer)

        elif int(variable_value) == 1 and int(variable_id[2:]) not in previus_state:
            state_answer = StateAnswer(previus_state.copy(), False, 0)
            statesList.append(state_answer)

        else:
            print("Caso borde: ", previus_state, variable_id, variable_value)


        return statesList
    
    def _probabilistic_function(self, variable_id):
        return self.values[variable_id]