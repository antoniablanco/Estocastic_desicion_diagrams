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
import dd_controller_generator.EstocasticDDKnapsack as EstocasticDDKnapsack
import dd_controller_generator.EstocasticDDKnapsack2 as EstocasticDDKnapsack2

@contextmanager
def assertNoRaise():
    try:
        yield
    except Exception as e:
        raise AssertionError(f"Se generó una excepción: {e}")

class ProblemKnapsackTest(unittest.TestCase):
    def setUp(self):
        class ProblemKnapsack(AbstractProblem):

            def __init__(self, initial_state, variables, list_of_wheight_for_restrictions, right_side_of_restrictions, values):
                super().__init__(initial_state, variables)

                self.list_of_wheight_for_restrictions = list_of_wheight_for_restrictions
                self.right_side_of_restrictions = right_side_of_restrictions
                self.values = values

            def equals(self, state_one, state_two):
                return state_one == state_two

            def transition_function(self, previus_state, variable_id, variable_value):
                statesList = []
                state_options = self._probabilistic_function(variable_id, variable_value)

                for state_option in state_options.keys():
                    new_state = int(previus_state[0]) + state_option*int(variable_value)
                    isFeasible = int(new_state) <= self.right_side_of_restrictions
                    probability = state_options[state_option]
                    
                    state_answer = StateAnswer([new_state], isFeasible, probability)
                    statesList.append(state_answer)

                return statesList
            
            def _probabilistic_function(self, variable_id, variable_value):
                return values[int(variable_value)][variable_id]
        
        matrix_of_wheight = [3, 3, 4, 6]
        right_side_of_restrictions = 5
        values = {
            0 : {'x_1': {0:1},
                 'x_2': {0:1},
                 'x_3': {0:1},
                 'x_4': {0:1}},

            1 : {'x_1': {1: 0.5, 2: 0.5},
                 'x_2': {2: 0.3, 3: 0.7},
                 'x_3': {1: 0.4, 4: 0.6},
                 'x_4': {3: 0.9, 4: 0.1} }
                }

        initial_state = [0]
        variables = [('x_1', [0, 1]), ('x_2', [0, 1]), ('x_3', [0, 1]), ('x_4', [0, 1])]
        self.problem_instance = ProblemKnapsack(initial_state, variables, matrix_of_wheight, right_side_of_restrictions, values)
        self.dd_instance = EstocasticDD(self.problem_instance, verbose=False)

    def test_ordered_variables(self):
        ordered_variables_test = ['x_1', 'x_2', 'x_3', 'x_4']
        self.assertEqual(self.problem_instance.ordered_variables, ordered_variables_test)
    
    def test_variables_domain(self):
        variables_domain_test = {'x_1': [0, 1], 'x_2': [0, 1], 'x_3': [0, 1], 'x_4': [0, 1]}
        self.assertEqual(self.problem_instance.variables_domain, variables_domain_test)

    def test_is_dd_created(self):
        self.assertIsNotNone(self.dd_instance.graph_DD)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_verbose_create_dd(self, mock_stdout):
        dd_instance = EstocasticDD(self.problem_instance, verbose=True)

        file_path = os.path.join('Test', 'test_prints', 'createEstocasticDDKnapsack.txt')
        
        with open(file_path, "r") as file:
            expected_output = file.read()

        actual_output = mock_stdout.getvalue()

        self.assertEqual(actual_output.strip(), expected_output.strip())
    
    def test_create_dd_graph_equal(self):
        resultado1 = self.dd_instance.graph_DD == EstocasticDDKnapsack.graph
        resultado2 = self.dd_instance.graph_DD == EstocasticDDKnapsack2.graph

        self.assertTrue(resultado1)
        self.assertTrue(resultado2)
    
    def test_get_dd_graph(self):
        self.assertIsNotNone(self.dd_instance.get_decision_diagram_graph())
    
    @patch('matplotlib.pyplot.show')
    def test_print_dd_graph(self, mock_show):
        dd_instance = EstocasticDD(self.problem_instance, verbose=False)

        with assertNoRaise():
            dd_instance.print_decision_diagram()
            mock_show.assert_called_once()
        
    def test_get_copy(self):
        dd_instance = EstocasticDD(self.problem_instance, verbose=False)
        self.assertIsNot(dd_instance.graph_DD, dd_instance.get_decision_diagram_graph_copy)

    def test_get_DDBuilder_time(self):
        dd_instance = EstocasticDD(self.problem_instance, verbose=False)
        self.assertTrue(dd_instance.get_estocasticDDBuilder_time()>0)
    
    def test_check_gml_file_content(self):
        dd_instance = EstocasticDD(self.problem_instance, verbose=False)
        dd_instance.export_graph_file('estocastic_test')

        expected_file_path = os.path.join('Test', 'gml_files', 'EstocasticKnapsackTest.gml')
        actual_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'estocastic_test.gml'))

        self.assertTrue(os.path.exists(actual_file_path))
        self.assertTrue(os.path.exists(expected_file_path))

        with open(expected_file_path, "r") as file:
            expected_output = file.read()
        
        with open(actual_file_path, "r") as file:
            actual_output = file.read()
        
        self.assertEqual(actual_output.strip(), expected_output.strip())
