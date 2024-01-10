import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

root_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(parent_dir)

from Class.Problems.AbstractProblemClass import AbstractProblem
from Class.AnswerEDD.StateAnswer import StateAnswer
from Exceptions.MyExceptions import SameLenError


class ProblemKnapsack(AbstractProblem):

    def __init__(self, initial_state, variables, 
    list_of_wheight_for_restrictions, right_side_of_restrictions, values):
        super().__init__(initial_state, variables)

        self.list_of_wheight_for_restrictions = list_of_wheight_for_restrictions
        self.right_side_of_restrictions = right_side_of_restrictions
        self.values = values
 
        self.check_atributes(variables, initial_state)

    def check_atributes(self, variables, initial_state):
        self.check_same_len_matrix_and_right_side(initial_state)
        self.check_same_len_rows_matrix_and_variables(variables)
        self.check_probabilities_sum_one()
    
    def check_same_len_matrix_and_right_side(self, initial_state):
        assert len(self.list_of_wheight_for_restrictions) == len(self.right_side_of_restrictions), "matrix_of_wheight and right_side_of_restrictions must have the same length"
        assert len(initial_state) == len(self.right_side_of_restrictions) or len(initial_state) == 2*len(self.right_side_of_restrictions), "matrix_of_wheight and right_side_of_restrictions must have the same length"
    
    def check_same_len_rows_matrix_and_variables(self, variables):
        for row in range(len(self.list_of_wheight_for_restrictions)):
            assert len(self.list_of_wheight_for_restrictions[row]) == len(variables), "rows of matrix_of_wheight and right_side_of_restrictions must have the same length of variables"

    def check_probabilities_sum_one(self):
        for variable in self.values.keys():
            for variable_value in self.values[variable].keys():
                assert sum(self.values[variable][variable_value].values()) == 1, "probabilities must sum 1"
    
    def equals(self, state_one, state_two):
        return state_one == state_two

    def transition_function(self, previus_state, variable_id, variable_value):
        statesList = []
        state_options = self._probabilistic_function(variable_id, variable_value)

        for state_option in state_options.keys():
            new_state = int(previus_state[0]) + state_option*int(variable_value)
            isFeasible = int(new_state) <= self.right_side_of_restrictions[0]
            probability = state_options[state_option]
            
            state_answer = StateAnswer([new_state], isFeasible, probability)
            statesList.append(state_answer)

        return statesList
    
    def merge_operator(self, state_one, state_two):
        state = []
        for i in range(len(state_one)):
            state.append([state_one[i][0], state_two[i][1]])
        return state

    def _probabilistic_function(self, variable_id, variable_value):
        return self.values[int(variable_value)][variable_id]