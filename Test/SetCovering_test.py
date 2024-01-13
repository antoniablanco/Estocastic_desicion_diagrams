import os
import sys
import io
import unittest
from unittest.mock import patch
from contextlib import contextmanager

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Class.Problems.AbstractProblemClass import AbstractProblem
from Class.EstocasticDD import EstocasticDD
from Class.AnswerEDD.StateAnswer import StateAnswer
import dd_controller_generator.EstocasticDDSetCovering as EstocasticDDSetCovering

@contextmanager
def assertNoRaise():
    try:
        yield
    except Exception as e:
        raise AssertionError(f"Se generó una excepción: {e}")
    

class ProblemSetCoveringTest(unittest.TestCase):
    def setUp(self):
        class ProblemSetCovering(AbstractProblem):

            def __init__(self, initial_state, variables, matrix_of_wheight, right_side_of_restrictions):
                super().__init__(initial_state, variables)

                self.matrix_of_wheight = matrix_of_wheight
                self.right_side_of_restrictions = right_side_of_restrictions
                self.max_positions = self.get_max_positions()
            
            def get_max_positions(self):
                max_positions = [-1, -1, -1]
                for j, row in enumerate(self.matrix_of_wheight):
                    for i, valor in enumerate(row[::-1]):
                        if valor != 0 and max_positions[j] == -1:
                            max_positions[j] = len(row) - i
                return max_positions

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

        initial_state = [1, 2, 3]
        variables = [('x_1', [0, 1]), ('x_2', [0, 1]), ('x_3', [0, 1]), ('x_4', [0, 1]), ('x_5', [0, 1])]

        matrix_of_wheight = [[1, 1, 0.2, 0, 0],
                            [0.3, 0, 0, 0.4, 1],
                            [0, 1, 0.7, 0.6, 0]]

        right_side_of_restrictions = [1, 1, 1]

        self.problem_instance = ProblemSetCovering(initial_state, variables, matrix_of_wheight, right_side_of_restrictions)
        self.dd_instance = EstocasticDD(self.problem_instance, verbose=False)

    def test_ordered_variables(self):
        ordered_variables_test = ['x_1', 'x_2', 'x_3', 'x_4', 'x_5']
        self.assertEqual(self.problem_instance.ordered_variables, ordered_variables_test)
    
    def test_variables_domain(self):
        variables_domain_test = {'x_1': [0, 1], 'x_2': [0, 1], 'x_3': [0, 1], 'x_4': [0, 1], 'x_5': [0, 1]}
        self.assertEqual(self.problem_instance.variables_domain, variables_domain_test)

    def test_is_dd_created(self):
        self.assertIsNotNone(self.dd_instance.graph_DD)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_verbose_create_dd(self, mock_stdout):
        dd_instance = EstocasticDD(self.problem_instance, verbose=True)

        file_path = os.path.join('Test', 'test_prints', 'createEstocasticDDSetCovering.txt')
        
        with open(file_path, "r") as file:
            expected_output = file.read()

        actual_output = mock_stdout.getvalue()

        self.assertEqual(actual_output.strip(), expected_output.strip())
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_verbose_create_reduce_dd(self, mock_stdout):
        self.dd_instance.reduce_estocastic_decision_diagram(verbose=True)

        file_path = os.path.join('Test', 'test_prints', 'createReduceDDSeCovering.txt')
        
        with open(file_path, "r") as file:
            expected_output = file.read()

        actual_output = mock_stdout.getvalue()

        self.assertEqual(actual_output.strip(), expected_output.strip())
    
    def test_create_dd_graph_equal(self):
        resultado = self.dd_instance.graph_DD == EstocasticDDSetCovering.graph
        self.assertTrue(resultado)
    
    def test_create_reduce_dd_graph_equal(self):
        self.dd_instance.reduce_estocastic_decision_diagram(verbose=False)
        resultado = self.dd_instance.graph_DD == EstocasticDDSetCovering.graph

        self.assertTrue(resultado)
    
    def test_get_dd_graph(self):
        self.assertIsNotNone(self.dd_instance.get_decision_diagram_graph())
    
    @patch('matplotlib.pyplot.show')
    def test_print_dd_graph(self, mock_show):

        with assertNoRaise():
            self.dd_instance.print_decision_diagram()
            mock_show.assert_called_once()
        
    @patch('matplotlib.pyplot.show')
    def test_print_reduce_dd_graph(self, mock_show):
        self.dd_instance.reduce_estocastic_decision_diagram(verbose=False)

        with assertNoRaise():
            self.dd_instance.print_decision_diagram()
            mock_show.assert_called_once()

    def test_get_copy(self):
        self.assertIsNot(self.dd_instance.graph_DD, self.dd_instance.get_decision_diagram_graph_copy)

    def test_get_dd_builder_time(self):
        self.assertTrue(self.dd_instance.get_estocastic_dd_time()>0)
    
    def test_get_reduce_dd_builder_time(self):
        self.dd_instance.reduce_estocastic_decision_diagram(verbose=False)
        time = self.dd_instance.get_reduce_estocastic_dd_time()
        self.assertTrue(time>0)
    
    def test_check_gml_file_content(self):
        dd_instance = EstocasticDD(self.problem_instance, verbose=False)
        dd_instance.export_graph_file('estocastic_test')

        expected_file_path = os.path.join('Test', 'gml_files', 'EstocasticSetCoveringTest.gml')
        actual_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'estocastic_test.gml'))

        self.assertTrue(os.path.exists(actual_file_path))
        self.assertTrue(os.path.exists(expected_file_path))

        with open(expected_file_path, "r") as file:
            expected_output = file.read()
        
        with open(actual_file_path, "r") as file:
            actual_output = file.read()
        
        self.assertEqual(actual_output.strip(), expected_output.strip())

    def test_check_gml_reduce_estocastic_dd(self):
        self.dd_instance.reduce_estocastic_decision_diagram(verbose=False)
        self.dd_instance.export_graph_file('estocastic_test')

        expected_file_path = os.path.join('Test', 'gml_files', 'ReduceSetCoveringTest.gml')
        actual_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'estocastic_test.gml'))

        self.assertTrue(os.path.exists(actual_file_path))
        self.assertTrue(os.path.exists(expected_file_path))

        with open(expected_file_path, "r") as file:
            expected_output = file.read()
        
        with open(actual_file_path, "r") as file:
            actual_output = file.read()
        
        self.assertEqual(actual_output.strip(), expected_output.strip())

    def test_get_correct_path_probability(self):

        self.assertEqual(self.dd_instance.get_path_probability({'x_1': 0, 'x_2': 0, 'x_3': 1, 'x_4': 1, 'x_5': 1}), 0.176)
        self.assertEqual(self.dd_instance.get_path_probability({'x_1': 1, 'x_2': 0, 'x_3': 1, 'x_4': 1, 'x_5': 1}), 0.88)
        self.assertEqual(self.dd_instance.get_path_probability({'x_1': 0, 'x_2': 0, 'x_3': 0, 'x_4': 0, 'x_5': 0}), 0)
        self.assertEqual(self.dd_instance.get_path_probability({'x_1': 1, 'x_2': 1, 'x_3': 1, 'x_4': 1, 'x_5': 1}), 1)