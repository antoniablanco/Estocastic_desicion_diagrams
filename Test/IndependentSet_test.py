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
import dd_controller_generator.EstocasticDDIndependentSet as EstocasticDDIndependentSet

@contextmanager
def assertNoRaise():
    try:
        yield
    except Exception as e:
        raise AssertionError(f"Se generó una excepción: {e}")

class ProblemIndependentSetTest(unittest.TestCase):
    def setUp(self):
        class ProblemIndependentSet(AbstractProblem):

            def __init__(self, initial_state, variables, dict_node_neighbors):
                super().__init__(initial_state, variables)
                self.dict_node_neighbors = dict_node_neighbors

            def equals(self, state_one, state_two):
                return set(state_one) == set(state_two)

            def transition_function(self, previus_state, variable_id, variable_value):
                statesList = []
                
                if int(variable_value) == 0 and int(variable_id[2:]) in previus_state:
                    new_state = previus_state.copy()
                    new_state.remove(int(variable_id[2:]))
                    statesList.append(StateAnswer(new_state, True, 1))
                    
                elif int(variable_value) == 0 and int(variable_id[2:]) not in previus_state:
                    statesList.append(StateAnswer(previus_state.copy(), True, 1))

                elif int(variable_value) == 1 and int(variable_id[2:]) in previus_state:
                    statesList = self._get_list_states_with_probabilities(previus_state, variable_id)

                elif int(variable_value) == 1 and int(variable_id[2:]) not in previus_state:
                    statesList.append(StateAnswer(previus_state.copy(), False, 0))

                return statesList
            
            def _get_list_states_with_probabilities(self, previus_state, variable_id):
                statesList = []
                static_state = previus_state.copy()
                static_state.remove(int(variable_id[2:]))
                possible_neighbors = []

                neighbors = self.dict_node_neighbors[variable_id]
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
                
                return statesList

        values = {  'x_1': {2: 1, 3: 1, 4: 0.1},
            'x_2': {1: 1, 3: 0.9, 4: 1},
            'x_3': {1: 1, 2: 0.9, 4: 0.8, 5: 0.2},
            'x_4': {1: 0.1, 2: 1, 3: 0.8},
            'x_5': {3: 0.2}}

        initial_state = [1, 2, 3, 4, 5]
        variables = [('x_1', [0, 1]), ('x_2', [0, 1]), ('x_3', [0, 1]), ('x_4', [0, 1]), ('x_5', [0, 1])]
        self.problem_instance = ProblemIndependentSet(initial_state, variables,values)
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

        file_path = os.path.join('Test', 'test_prints', 'createEstocasticDDIndependentSet.txt')
        
        with open(file_path, "r") as file:
            expected_output = file.read()

        actual_output = mock_stdout.getvalue()

        self.assertEqual(actual_output.strip(), expected_output.strip())
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_verbose_create_reduce_dd(self, mock_stdout):
        self.dd_instance.reduce_estocastic_decision_diagram(verbose=True)

        file_path = os.path.join('Test', 'test_prints', 'createReduceDDIndependentSet.txt')
        
        with open(file_path, "r") as file:
            expected_output = file.read()

        actual_output = mock_stdout.getvalue()

        self.assertEqual(actual_output.strip(), expected_output.strip())
    
    def test_create_dd_graph_equal(self):
        resultado = self.dd_instance.graph_DD == EstocasticDDIndependentSet.graph
        self.assertTrue(resultado)
    
    def test_create_reduce_dd_graph_equal(self):
        self.dd_instance.reduce_estocastic_decision_diagram(verbose=False)
        resultado = self.dd_instance.graph_DD == EstocasticDDIndependentSet.graph

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

        expected_file_path = os.path.join('Test', 'gml_files', 'EstocasticIndependentSetTest.gml')
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

        expected_file_path = os.path.join('Test', 'gml_files', 'ReduceIndependentSetTest.gml')
        actual_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'estocastic_test.gml'))

        self.assertTrue(os.path.exists(actual_file_path))
        self.assertTrue(os.path.exists(expected_file_path))

        with open(expected_file_path, "r") as file:
            expected_output = file.read()
        
        with open(actual_file_path, "r") as file:
            actual_output = file.read()
        
        self.assertEqual(actual_output.strip(), expected_output.strip())
