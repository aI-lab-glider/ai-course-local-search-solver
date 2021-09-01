from typing import Any, Iterable, Tuple
from genetic_algorithms.problems.base.moves import Move
from genetic_algorithms.problems.base import Model, State
from genetic_algorithms.helpers import History
from genetic_algorithms.solvers.solver import Solver


class LocalSearchSolver(Solver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = History[int](self.config.history_size)

    def solve(self, model: Model) -> State:
        solution = model.initial_solution
        moves, solution_cost = self._update(model, state=solution)
        iter_count = 0
        self.history.append(solution_cost)
        while not self.is_extremum(solution_cost) and iter_count < self.config.max_iter:
            solution = self._hill_climbing(model, solution, moves)
            moves, solution_cost = self._update(model, solution)
            iter_count += 1
        return solution

    def _update(self, model: Model, state: State) -> Tuple[Iterable[Move[Any]], int]:
        moves = model.moves_for(state)
        cost = model.cost_for(state)
        return moves, cost

    def _hill_climbing(self, model: Model, state: State, available_moves: Iterable[Move[Any]]) -> State:
        best_state = state
        best_state_cost = model.cost_for(state)
        for move in available_moves:
            new_state = move.make()
            new_state_cost = model.cost_for(new_state)
            if new_state_cost <= best_state_cost:
                (best_state, best_state_cost) = (new_state, new_state_cost)
        return best_state

    def is_extremum(self, cost_to_check: int):
        return all(cost == cost_to_check for cost in self.history) and self.history.is_full()
