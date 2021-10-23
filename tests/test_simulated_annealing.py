import random
from unittest.mock import patch

import pytest

from local_search.algorithms.simulated_annealing import SimulatedAnnealing
from test_utils import create_object_copy_with_student_method
from tests.mock import MockGoalMax, MockProblem, MockState

PROBLEM_SIZE = 100


@pytest.fixture
def student_solver(student_loader, method_name: str) -> SimulatedAnnealing:
    teacher_solver = SimulatedAnnealing()
    return create_object_copy_with_student_method(teacher_solver,
                                                  student_loader,
                                                  "local_search/algorithms/simulated_annealing.py",
                                                  method_name)


@pytest.mark.parametrize('method_name', [SimulatedAnnealing._reheat.__name__])
def test_reheat_should_restore_temp_and_reset_schedule(student_solver, record_property):
    record_property("points", 2)
    student_solver.temperature = 0
    student_solver.steps_from_last_state_update = 100
    student_solver.cooling_time = 100
    state = MockState.suboptimal_state()
    new_state = student_solver._reheat(state)
    assert state == new_state, "reheating modifies the state, it shouldn't!"
    print(student_solver.config)
    expected_temp = student_solver.config.escape_reheat_ratio * \
                    student_solver.config.initial_temperature
    assert student_solver.temperature == expected_temp, f"reheating should change temperature according to " \
                                                        f"self.config, got {student_solver.temperature}, " \
                                                        f"expected {expected_temp}"
    assert student_solver.steps_from_last_state_update == 0, "reheating should reset the " \
                                                             "'steps_from_last_state_update' "
    assert student_solver.cooling_time == 0, "reheating should reset the 'cooling_time'"


@pytest.mark.parametrize('method_name', [SimulatedAnnealing._update_temperature.__name__])
def test_update_temperature_not_goes_below_min_temperature(student_solver: SimulatedAnnealing, set_random_seed):
    student_solver.config.min_temperature = 1
    student_solver.temperature = 0.9 * student_solver.config.min_temperature
    student_solver.cooling_time = random.randint(1, 5)
    student_solver.config.cooling_step = random.random()
    student_solver._update_temperature()
    assert student_solver.temperature == student_solver.config.min_temperature, 'update temperature should not go below min' \
                                                                                'temperature during update'


@pytest.mark.parametrize('method_name', [SimulatedAnnealing._update_temperature.__name__])
def test_update_temperature_uses_correct_decrease_function(student_solver: SimulatedAnnealing):
    teacher_solver = SimulatedAnnealing()
    student_solver.config = teacher_solver.config
    initial_temperature = student_solver.temperature = teacher_solver.temperature
    initial_cooling_time = student_solver.cooling_time = teacher_solver.cooling_time
    teacher_solver._update_temperature()
    student_solver._update_temperature()
    assert student_solver.temperature == teacher_solver.temperature, 'update temperature, does not uses correct formula to update temperature:' \
                                                                     'for params:' \
                                                                     f'temperature: {initial_temperature}' \
                                                                     f'cooling_time: {initial_cooling_time}' \
                                                                     f'cooling_step: {teacher_solver.config.cooling_step}' \
                                                                     f'expected new temperature to be: {teacher_solver.temperature}' \
                                                                     f'but received: {student_solver.temperature}'


@pytest.mark.parametrize('method_name', [SimulatedAnnealing._update_temperature.__name__])
def test_update_temperature_updates_cooling_time(student_solver: SimulatedAnnealing, record_property):
    record_property("points", 2)
    INITIAL_COOLING_TIME = 1
    student_solver.cooling_time = INITIAL_COOLING_TIME
    student_solver._update_temperature()
    assert student_solver.cooling_time == INITIAL_COOLING_TIME + 1, 'expected update temperature to  update cooling time by 1,' \
                                                                    f'not by {student_solver.cooling_time - INITIAL_COOLING_TIME}'


@pytest.mark.parametrize('method_name', [SimulatedAnnealing._calculate_transition_probability.__name__])
@pytest.mark.parametrize('mocked_improvement', [
    10 ** i for i in range(4)
])
def test_calculate_transition_probability(student_solver: SimulatedAnnealing, mocked_improvement, record_property):
    class MockProblem:
        def improvement(*args):
            return mocked_improvement

    problem = MockProblem()
    teacher_solver = SimulatedAnnealing()
    initial_temp = teacher_solver.temperature = student_solver.temperature = 1
    expected_probability = teacher_solver._calculate_transition_probability(
        problem, None, None)
    actual_probability = student_solver._calculate_transition_probability(
        problem, None, None)
    assert expected_probability == actual_probability, f'expected to calculate {expected_probability}' \
                                                       f'for delta model improvement {mocked_improvement} amd temperature {initial_temp}'


@pytest.mark.parametrize('method_name', [SimulatedAnnealing._find_next_state.__name__])
def test_find_next_state_gets_random_neighbour(student_solver: SimulatedAnnealing, set_random_seed, record_property):
    record_property("points", 2)
    model = MockProblem(PROBLEM_SIZE, MockGoalMax())
    initial_state = MockState.suboptimal_state(PROBLEM_SIZE)
    with patch.object(student_solver, SimulatedAnnealing._get_random_neighbours.__name__):
        student_solver._get_random_neighbours.return_value = (
            s for s in [initial_state])
        _ = student_solver._find_next_state(model, initial_state)
        student_solver._get_random_neighbours.assert_called_once_with(
            model, initial_state)


@pytest.mark.parametrize('method_name', [SimulatedAnnealing._find_next_state.__name__])
def test_find_next_state_returns_next_state_if_state_is_better(student_solver: SimulatedAnnealing, set_random_seed,
                                                               record_property):
    record_property("points", 2)
    model = MockProblem(PROBLEM_SIZE, MockGoalMax())
    state = MockState.suboptimal_state(PROBLEM_SIZE)
    optimal_state = MockState.optimal_state(model.goal.type(), model.sum)
    with patch.object(student_solver, SimulatedAnnealing._get_random_neighbours.__name__):
        student_solver._get_random_neighbours.return_value = (
            s for s in [optimal_state])
        next_state = student_solver._find_next_state(model, state)
    assert next_state == optimal_state, 'expected algorithm to select improving state'


@pytest.mark.parametrize('method_name', [SimulatedAnnealing._find_next_state.__name__])
def test_find_next_state_calculates_transition_probability_if_state_is_not_better(student_solver: SimulatedAnnealing,
                                                                                  set_random_seed, record_property):
    record_property("points", 2)
    model = MockProblem(PROBLEM_SIZE, MockGoalMax())
    state = MockState.optimal_state(model.goal.type(), PROBLEM_SIZE)
    next_state = MockState.suboptimal_state(PROBLEM_SIZE)
    with patch.object(student_solver, SimulatedAnnealing._calculate_transition_probability.__name__), \
            patch.object(student_solver, SimulatedAnnealing._get_random_neighbours.__name__):
        student_solver._get_random_neighbours.return_value = (
            s for s in [next_state])
        student_solver._calculate_transition_probability.return_value = 1
        _ = student_solver._find_next_state(model, state)
        student_solver._calculate_transition_probability.assert_called_once_with(
            model, state, next_state)


@pytest.mark.parametrize('method_name', [SimulatedAnnealing._find_next_state.__name__])
def test_find_next_state_updates_temperatures(student_solver, record_property):
    record_property("points", 2)
    model = MockProblem(PROBLEM_SIZE, MockGoalMax())
    state = MockState.suboptimal_state(PROBLEM_SIZE)
    with patch.object(student_solver, SimulatedAnnealing._update_temperature.__name__):
        _ = student_solver._find_next_state(model, state)
        student_solver._update_temperature.assert_called_once()
