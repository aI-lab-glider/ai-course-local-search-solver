from dataclasses import dataclass
from genetic_algorithms.models.next_state_provider import NextStateProvider
from genetic_algorithms.models.algorithm import Algorithm
from genetic_algorithms.solvers.local_search_solver import LocalSearchSolver
from genetic_algorithms.solvers.solver import SolverConfig
from genetic_algorithms.helpers import History
from genetic_algorithms.problems.base import Model, State
from random import randint
from copy import deepcopy


@dataclass
class SolverWithRandomRestartsConfig(SolverConfig):
    num_restarts: int = 5
    max_distance_from_initial_solution: int = 100


class LocalSearchSolverWithRandomRestarts(LocalSearchSolver):
    """
    Solver which adopts the adage, “If at first you Random-restart hill climbing
    don’t succeed, try, try again.”

    It conducts a series of hill-climbing searches from randomly generated initial states,
    until a goal is found.
    """

    def __init__(self, config: SolverWithRandomRestartsConfig, **kwargs):
        super().__init__(config=config, **kwargs)
        self._stored_solutions = History[State](config.num_restarts)

    def _is_goal_found(self) -> bool:
        # TODO cover with tests, because it is error prone: we don't know what can be done
        # with this history higher.
        return self.cost_history.is_full() and len(set(self.cost_history)) == 1

    def _create_model_with_new_initial_state(self, from_model: Model) -> Model:

        num_moves = randint(0, self.config.max_distance_from_initial_solution)
        new_model = deepcopy(from_model)
        for _ in range(num_moves):
            first_move = next(new_model.move_generator.random_moves(
                new_model.initial_solution))
            new_model.initial_solution = first_move.make()
        return new_model

    def solve(self, model: Model, algorithm: NextStateProvider) -> State:
        while not self._stored_solutions.is_full() and not self._is_goal_found():
            solution = super().solve(model, algorithm)
            self._stored_solutions.append(solution)
            model = self._create_model_with_new_initial_state(from_model=model)
        return sorted(self._stored_solutions, key=lambda s: model.cost_for(s), reverse=True)[0]
