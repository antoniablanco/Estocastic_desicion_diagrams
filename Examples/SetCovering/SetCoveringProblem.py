import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

root_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(parent_dir)

from Class.Problems.AbstractProblemClass import AbstractProblem
from Class.AnswerEDD.StateAnswer import StateAnswer


class SetCoveringProblem(AbstractProblem):

    def __init__(self, initial_state, variables, matrix_of_wheight, right_side_of_restrictions):
        super().__init__(initial_state, variables)

        self.matrix_of_wheight = matrix_of_wheight
        self.right_side_of_restrictions = right_side_of_restrictions
        self.max_positions = self.get_max_positions()

        self.check_atributes(variables, initial_state)
    
    def get_max_positions(self):
        max_positions = [-1, -1, -1]
        for j, row in enumerate(self.matrix_of_wheight):
            for i, valor in enumerate(row[::-1]):
                if valor != 0 and max_positions[j] == -1:
                    max_positions[j] = len(row) - i
        return max_positions

    def check_atributes(self, variables, initial_state):
        self.check_same_len_matrix_and_right_side(initial_state)
        self.check_same_len_rows_matrix_and_variables(variables)
        self.check_values_must_be_in_range()
    
    def check_same_len_matrix_and_right_side(self, initial_state):
        assert len(self.matrix_of_wheight) == len(self.right_side_of_restrictions), "matrix_of_wheight and right_side_of_restrictions must have the same length"
        assert len(initial_state) == len(self.right_side_of_restrictions) or len(initial_state) == 2*len(self.right_side_of_restrictions), "matrix_of_wheight and right_side_of_restrictions must have the same length"
    
    def check_same_len_rows_matrix_and_variables(self, variables):
        for row in range(len(self.matrix_of_wheight)):
            assert len(self.matrix_of_wheight[row]) == len(variables), "rows of matrix_of_wheight and right_side_of_restrictions must have the same length of variables"

    def check_values_must_be_in_range(self):
        for i, row in enumerate(self.matrix_of_wheight):
            if not any(valor != 0 for valor in row):
                raise ValueError(f"Invalid entry for row {i}: At least one value must be greater than 0")
            for value in row:
                if not (0 <= value <= 1):
                    raise ValueError(f"Invalid entry for row {i}: Value must be an integer, and  be in the range [0, 1. Got {value}")

    def equals(self, state_one, state_two):
        return set(state_one) == set(state_two)

    def transition_function(self, previous_state, variable_id, variable_value):
        statesList = []

        if int(variable_value) == 0:
            isFeasible = True 
            new_state = previous_state.copy()
            for row in previous_state: 
                if int(variable_id[2:]) >= self.max_positions[row-1]:
                    isFeasible = False 
            statesList.append(StateAnswer(new_state, isFeasible, 1.0))

        else:
            statesList = self._get_list_states_with_probabilities(previous_state, variable_id)
        
        return statesList
    
    def _get_list_states_with_probabilities(self, previous_state, variable_id):
        statesList = []
        variable_position = int(variable_id[2:])-1
        dinamic = [i for i in previous_state if self.matrix_of_wheight[i-1][variable_position] < 1 and self.matrix_of_wheight[i-1][variable_position] > 0]
        static = [i for i in previous_state if self.matrix_of_wheight[i-1][variable_position] == 0]

        for bitset in range(1<<len(dinamic)):
            probability = 1.0
            isFeasible = True
            new_state = static.copy()

            for i in range(len(dinamic)):
                if bitset & (1 << i):
                    probability *= self.matrix_of_wheight[dinamic[i] - 1][variable_position]

                else:
                    new_state.append(dinamic[i])

                    probability *= 1 - self.matrix_of_wheight[dinamic[i]-1][variable_position]
                    if int(variable_id[2:]) >= self.max_positions[dinamic[i]-1]:
                        isFeasible = False

            probability = round(probability, 4)
            new_state.sort()
            statesList.append(StateAnswer(new_state, isFeasible, probability))
        return statesList
        