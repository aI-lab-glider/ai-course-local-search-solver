from typing import List
from genetic_algorithms.problems.base.moves import Move
from genetic_algorithms.problems.base import Model, State
from genetic_algorithms.helpers import History
from genetic_algorithms.solvers.solver import Solver


class LocalSearchSolver(Solver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = History[int](self.config.history_size)

    def solve(self, problem: Model) -> State:
        moves = problem.valid_moves
        solution = problem.initial_solution
        solution_cost = problem.cost_for(solution)
        iter_count = 0
        self.history.append(solution_cost)
        while not self.is_local_minimum(solution_cost) and iter_count < self.config.max_iter:
            solution = self._local_search(problem, solution, moves)
            iter_count += 1
        return solution

    def _local_search(self, model: Model, state: State, moves: List[Move]) -> State:
        best_state = state
        best_state_cost = model.cost_for(state)
        violations = sorted(model.find_violations_in(
            state), reverse=True, key=lambda v: v.cost)
        violation_to_fix = violations[0]
        for move in moves:
            binded_move = move.bind_to(state)
            new_state = binded_move.make_on(violation_to_fix.decision_variable)
            new_state_cost = model.cost_for(new_state)
            if new_state_cost <= best_state_cost:
                (best_state, best_state_cost) = (new_state, best_state_cost)
        return best_state

    def is_local_minimum(self, cost_to_check: int):
        return all(cost == cost_to_check for cost in self.history) and self.history.is_full()
