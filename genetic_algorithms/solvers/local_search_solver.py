from typing import Any, Iterable, Tuple
from genetic_algorithms.problems.base.moves import Move
from genetic_algorithms.problems.base import Model, State
from genetic_algorithms.helpers import History
from genetic_algorithms.solvers.solver import Solver
from genetic_algorithms.models.algorithm import Algorithm


class LocalSearchSolver(Solver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = History[int](self.config.history_size)

    def solve(self, model: Model, algorithm: Algorithm) -> State:
        solution = model.initial_solution
        solution_cost = self._update(model, state=solution)
        iter_count = 0
        self.history.append(solution_cost)
        while not self.is_extremum(solution_cost) and iter_count < self.config.max_iter:
            solution = algorithm.next_state(model, solution)
            solution_cost = self._update(model, solution)
            iter_count += 1
        return solution

    def _update(self, model: Model, state: State) -> int:
        cost = model.cost_for(state)
        return cost

    def is_extremum(self, cost_to_check: int):
        return all(cost == cost_to_check for cost in self.history) and self.history.is_full()
