import pytest
from local_search.algorithms.hill_climbing.best_choice_hill_climbing import BestChoiceHillClimbing
from local_search.algorithms.hill_climbing.hill_climbing import HillClimbing, DEFAULT_CONFIG
from local_search.algorithms.hill_climbing.random_choice_hill_climbing import RandomChoiceHillClimbing
from local_search.algorithms.hill_climbing.worst_choice_hill_climbing import WorstChoiceHillClimbing
from tests.sum_problem import SumProblem, SumProblemGoal, Maximize, Minimize, SumProblemState


# TODO: should be here?
PROBLEM_SIZE = 100


@pytest.fixture
def goals() -> list[SumProblemGoal]:
    return [Minimize(), Maximize()]


def test_best_choice_hill_climbing_should_find_the_best_neighbour(goals: list[SumProblemGoal]):
    solver = BestChoiceHillClimbing(DEFAULT_CONFIG)
    for goal in goals:
        state = SumProblemState.suboptimal_state(PROBLEM_SIZE)
        next_state, problem = get_climbing_results_for_a_mock_problem(
            solver, goal, state)
        assert problem.improvement(next_state,
                                   state) > 0, "algorithm returns a state that's not better than the previous " \
                                               f"one (goal type: {goal.type()})"

        next_states = problem.next_states_from(state)
        improving_states = [
            s for s in next_states if problem.improvement(s, state) > 0]
        expected_state = max(
            improving_states, key=lambda next_state: problem.improvement(next_state, state))
        assert problem.objective_for(next_state) == problem.objective_for(
            expected_state), "algorithm does return an improving state, but it's not the best " \
            f"(goal type: {goal.type()})"


def test_random_choice_hill_climbing_should_find_the_random_improving_neighbour(goals):
    solver = RandomChoiceHillClimbing(DEFAULT_CONFIG)
    for goal in goals:
        state = SumProblemState.suboptimal_state(PROBLEM_SIZE)

        next_state, problem = get_climbing_results_for_a_mock_problem(
            solver, goal, state)
        assert problem.improvement(next_state, state) >= 0, f"algorithm returns a state that's worse than " \
            f"the previous " \
            "one (goal type: {goal.type()})"

        next_values = set([problem.objective_for(
            solver._climb_the_hill(problem, state)) for _ in range(100)])
        assert len(
            next_values) > 1, f"algorithm is deterministic, always returns the same state, while it should be random " \
            f"(goal type: {goal.type()})) "


def get_climbing_results_for_a_mock_problem(solver: HillClimbing, goal: SumProblemGoal, state: SumProblemState):
    problem = SumProblem(PROBLEM_SIZE, goal)
    next_state = solver._climb_the_hill(problem, state)
    assert next_state is not None, "algorithm returns None instead of a state"
    return next_state, problem
