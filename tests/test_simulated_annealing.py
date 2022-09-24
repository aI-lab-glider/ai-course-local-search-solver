from http.cookies import SimpleCookie
import random
from unittest.mock import patch

import pytest

from local_search.algorithms.simulated_annealing import SimulatedAnnealing
from tests.sum_problem import Maximize, SumProblem, SumProblemState
from mpmath import mpf

PROBLEM_SIZE = 100


def test_reheat_should_restore_temp_and_reset_schedule():
    solver = SimulatedAnnealing()
    solver.temperature = 0
    solver.steps_from_last_state_update = 100
    solver.cooling_time = 100
    state = SumProblemState.suboptimal_state()
    new_state = solver._reheat(state)
    assert state == new_state, "reheating modifies the state, it shouldn't!"
    expected_temp = solver.config.escape_reheat_ratio * \
        solver.config.initial_temperature
    assert solver.temperature == expected_temp, f"reheating should change temperature according to " \
        f"self.config, got {solver.temperature}, " \
        f"expected {expected_temp}"
    assert solver.steps_from_last_state_update == 0, "reheating should reset the " \
        "'steps_from_last_state_update' "
    assert solver.cooling_time == 0, "reheating should reset the 'cooling_time'"


def test_update_temperature_not_goes_below_min_temperature():
    random.seed(42)
    solver = SimulatedAnnealing()
    solver.config.min_temperature = 1
    solver.temperature = 0.9 * solver.config.min_temperature
    solver.cooling_time = random.randint(1, 5)
    solver.config.cooling_step = random.random()
    solver._update_temperature()
    assert solver.temperature == solver.config.min_temperature, 'update temperature should not go below min' \
        'temperature during update'


def test_update_temperature_uses_correct_decrease_function():
    solver = SimulatedAnnealing()
    initial_temperature = solver.config.initial_temperature
    initial_cooling_time = solver.cooling_time
    solver._update_temperature()
    expected_temperature = 5
    assert solver.temperature == expected_temperature, 'update temperature, does not uses correct formula to update temperature:' \
        'for params:' \
        f'temperature: {initial_temperature}' \
        f'cooling_time: {initial_cooling_time}' \
        f'cooling_step: {solver.config.cooling_step}' \
        f'expected new temperature to be: {expected_temperature}' \
        f'but received: {solver.temperature}'


def test_update_temperature_updates_cooling_time():
    INITIAL_COOLING_TIME = 1
    solver = SimulatedAnnealing()
    solver.cooling_time = INITIAL_COOLING_TIME
    solver._update_temperature()
    assert solver.cooling_time == INITIAL_COOLING_TIME + 1, 'expected update temperature to  update cooling time by 1,' \
        f'not by {solver.cooling_time - INITIAL_COOLING_TIME}'


@pytest.mark.parametrize('mocked_improvement, expected_probability', zip([
    10 ** i for i in range(2)
], [mpf('2.7182818284590451'), mpf('22026.465794806718')]))
def test_calculate_transition_probability(mocked_improvement, expected_probability):
    class TestProblem:
        def improvement(*args):
            return mocked_improvement

    problem = TestProblem()
    solver = SimulatedAnnealing()
    initial_temp = solver.temperature = 1
    actual_probability = solver._calculate_transition_probability(
        problem, None, None)
    assert expected_probability == actual_probability, f'expected to calculate {expected_probability}' \
                                                       f'for delta model improvement {mocked_improvement} and temperature {initial_temp}'


def test_find_next_state_gets_random_neighbour():
    random.seed(42)
    solver = SimulatedAnnealing()
    model = SumProblem(PROBLEM_SIZE, Maximize())
    initial_state = SumProblemState.suboptimal_state(PROBLEM_SIZE)
    with patch.object(solver, SimulatedAnnealing._get_random_neighbours.__name__):
        solver._get_random_neighbours.return_value = (
            s for s in [initial_state])
        _ = solver._find_next_state(model, initial_state)
        solver._get_random_neighbours.assert_called_once_with(
            model, initial_state)


def test_find_next_state_returns_next_state_if_state_is_better():
    solver = SimulatedAnnealing()
    model = SumProblem(PROBLEM_SIZE, Maximize())
    state = SumProblemState.suboptimal_state(PROBLEM_SIZE)
    optimal_state = SumProblemState.optimal_state(model.goal.type(), model.sum)
    with patch.object(solver, SimulatedAnnealing._get_random_neighbours.__name__):
        solver._get_random_neighbours.return_value = (
            s for s in [optimal_state])
        next_state = solver._find_next_state(model, state)
    assert next_state == optimal_state, 'expected algorithm to select improving state'


def test_find_next_state_calculates_transition_probability_if_state_is_not_better():
    solver = SimulatedAnnealing()
    model = SumProblem(PROBLEM_SIZE, Maximize())
    state = SumProblemState.optimal_state(model.goal.type(), PROBLEM_SIZE)
    next_state = SumProblemState.suboptimal_state(PROBLEM_SIZE)
    with patch.object(solver, SimulatedAnnealing._calculate_transition_probability.__name__), \
            patch.object(solver, SimulatedAnnealing._get_random_neighbours.__name__):
        solver._get_random_neighbours.return_value = (
            s for s in [next_state])
        solver._calculate_transition_probability.return_value = 1
        _ = solver._find_next_state(model, state)
        solver._calculate_transition_probability.assert_called_once_with(
            model, state, next_state)


def test_find_next_state_updates_temperatures():
    solver = SimulatedAnnealing()
    model = SumProblem(PROBLEM_SIZE, Maximize())
    state = SumProblemState.suboptimal_state(PROBLEM_SIZE)
    with patch.object(solver, SimulatedAnnealing._update_temperature.__name__):
        _ = solver._find_next_state(model, state)
        solver._update_temperature.assert_called_once()
