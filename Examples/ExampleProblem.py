import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

root_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(parent_dir)

from Class.Problems.AbstractProblemClass import AbstractProblem
from Exceptions.MyExceptions import SameLenError


class ProblemKnapsack(AbstractProblem):

    def __init__(self, initial_state, variables, list_of_wheight_for_restrictions, right_side_of_restrictions):
        super().__init__(initial_state, variables)

        self.list_of_wheight_for_restrictions = list_of_wheight_for_restrictions
        self.right_side_of_restrictions = right_side_of_restrictions

        #self.check_atributes(variables, initial_state)

    def check_atributes(self, variables, initial_state):
        self.check_same_len_matrix_and_right_side(initial_state)
        self.check_same_len_rows_matrix_and_variables(variables)
    
    def check_same_len_matrix_and_right_side(self, initial_state):
        assert len(self.list_of_wheight_for_restrictions) == len(self.right_side_of_restrictions), "matrix_of_wheight and right_side_of_restrictions must have the same length"
        assert len(initial_state) == len(self.right_side_of_restrictions) or len(initial_state) == 2*len(self.right_side_of_restrictions), "matrix_of_wheight and right_side_of_restrictions must have the same length"
    
    def check_same_len_rows_matrix_and_variables(self, variables):
        for row in range(len(self.list_of_wheight_for_restrictions)):
            assert len(self.list_of_wheight_for_restrictions[row]) == len(variables), "rows of matrix_of_wheight and right_side_of_restrictions must have the same length of variables"

    def equals(self, state_one, state_two):
        return state_one == state_two

    def transition_function(self, previus_state, variable_id, variable_value):
        # Cada row es una lista de 3 elementos: [new_state, probability, isFeasible]
        states = []
        state_options = self._probabilistic_function(variable_id, variable_value)

        for state_option in state_options.keys():
            new_state = int(previus_state[0]) + state_option*int(variable_value)
            isFeasible = int(new_state) <= self.right_side_of_restrictions
            probability = state_options[state_option]
            states.append([[new_state], probability, isFeasible])

        return states
    
    def _probabilistic_function(self, variable_id, variable_value):
        values = [
            {1: 0.5, 2: 0.5},
            {2: 0.3, 3: 0.7},
            {1: 0.4, 4: 0.6},
            {3: 0.9, 4: 0.1} 
        ]

        if int(variable_value) == 0:
            return {0: 1}

        return values[int(variable_id[2:])-1]